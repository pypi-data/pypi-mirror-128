import os
import torch
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import LambdaLR
import numpy as np

from vietvoice.model.tacotron2 import Tacotron2, Tacotron2Loss
from vietvoice.loader import TextMelCollate, TextMelLoader, save_mel 
from vietvoice.utils.lr_decay import get_linear_lambda_with_warmup
from vietvoice.utils.visualize import plot_loss, plot_output
from vietvoice.utils.logger import Logger
from vietvoice.utils.download_model import download_weights, map_state_dict
from vietvoice.symbol import Symbol

class Trainer():
    def __init__(self, config):
        
        train_config = config['train_config']
        symbols_config = config['symbols_config']
        data_config = config['data_config']
        encoder_config = config['encoder_config']
        decoder_config = config['decoder_config']
        postnet_config = config['postnet_config']

        self.device = train_config['device']
        self.batch_size = train_config['batch_size']
        self.precomputed_mels = train_config['precomputed_mels']
        self.num_iters = train_config['num_iters']
        self.eval_steps = train_config['eval_steps']
        self.warmup_steps = train_config['warmup_steps']
        self.log_dir = train_config['log_dir']
        
        self.symbols = Symbol(**symbols_config)

        if self.precomputed_mels != None:
            print('Mels will load from precomputed mels insteads of compute directly from audio')
            if os.path.isdir(self.precomputed_mels):
                print('Warning !!! {} existed. Please remove if you want to recaculate again.'.format(self.precomputed_mels))
            else:
                save_mel(train_config['train_files'], train_config['precomputed_mels'], data_config)
                save_mel(train_config['test_files'], train_config['precomputed_mels'], data_config)

        collate_fn = TextMelCollate()

        trainset = TextMelLoader(train_config['train_files'], text_to_index_fn=self.symbols,
                                 precomputed_mels = train_config['precomputed_mels'],
                                **data_config)

        self.train_loader = DataLoader(trainset, num_workers=3, shuffle=True,
                                  sampler=None,
                                  batch_size=train_config['batch_size'], pin_memory=False,
                                  drop_last=True, collate_fn=collate_fn)

        self.train_iter = iter(self.train_loader)

        evalset = TextMelLoader(train_config['test_files'], text_to_index_fn=self.symbols,
                                precomputed_mels = train_config['precomputed_mels'],
                                **data_config)

        self.eval_loader = DataLoader(evalset, num_workers=1, shuffle=False,
                                  sampler=None,
                                  batch_size=train_config['batch_size'], pin_memory=False,
                                  drop_last=True, collate_fn=collate_fn)
        
        self.model = Tacotron2(n_mel_channels=data_config['n_mel_channels'], 
                  n_frames_per_step=data_config['n_frames_per_step'],
                  drop_frame_rate=train_config['drop_frame_rate'], 
                  global_mean=self.global_mean(data_config), 
                  n_symbols = len(self.symbols),
                  symbols_embedding_dim= symbols_config['symbols_embedding_dim'],
                  encoder_config=encoder_config, 
                  decoder_config=decoder_config, 
                  postnet_config=postnet_config)
        
        sample_batch = next(iter(self.eval_loader))
        sample_x, sample_y = self.model.parse_input(sample_batch, self.device)
        self.sample_text_inputs, self.sample_text_lengths, self.sample_mels, self.sample_output_lengths = sample_x

        if self.device.startswith('cuda'):
            self.model = self.model.to(self.device)
        
        self.criterion = Tacotron2Loss()
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=train_config['learning_rate'],
                                 weight_decay=1e-6)

        self.lr_lambda = get_linear_lambda_with_warmup(self.warmup_steps, self.num_iters)
        self.scheduler = LambdaLR(self.optimizer, self.lr_lambda)

        self.best_eval_loss = 99999
        self.current_iter = 0
        self.train_losses = []
        self.eval_losses = []
        
        if self.log_dir != None:
            self.log = Logger(os.path.join(self.log_dir, 'log.txt'))
        
        pretrained = train_config['pretrained_url']
        if pretrained != None:
            print('Load pretrained model')
            pretrained_weights_path = download_weights(pretrained, md5=train_config['pretrained_md5'])
            state_dict = torch.load(pretrained_weights_path)
            state_dict = map_state_dict(self.model, state_dict)
            self.model.load_state_dict(state_dict, strict=False)

    def train(self):
        for i in range(self.current_iter, self.num_iters):
            self.current_iter = i
            try:
                batch = next(self.train_iter)
            except StopIteration:
                self.train_iter = iter(self.train_loader)
                batch = next(self.train_iter)
            
            x, y = self.model.parse_input(batch, self.device)
            
            loss_items = self.train_step(x, y, i)
            str_log = 'Iter: {:06d} - total loss: {:.6f} - mel loss: {:.6f} - gate loss: {:.6f} - alignemnt loss: {:.6f} - lr: {:.2e}'.format(i, *loss_items, self.optimizer.param_groups[0]['lr'])
            self.log(str_log)

            if i >= 1000:
                self.train_losses.append((i, *loss_items))
            
            if i % self.eval_steps == 0:
                eval_loss_items = self.evaluate()
                self.sample()

                self.eval_losses.append((i, *eval_loss_items))

                plot_loss(self.train_losses, 'train_loss', self.log_dir)
                plot_loss(self.eval_losses, 'eval_loss', self.log_dir)
                
                str_log = 'evaluation: iter: {:06d} - total loss: {:.6f} - mel loss: {:.6f} - gate loss: {:.6f} - alignemnt loss: {:.6f}'.format(i, *eval_loss_items)
                self.log(str_log)

                if eval_loss_items[0] < self.best_eval_loss:
                    self.best_eval_loss = eval_loss_items[0]
                    self.save_checkpoint()

    def train_step(self, x, y, i):
        self.model.train()
        self.model.zero_grad()
        guide_decay = self.lr_lambda(i)

        y_pred = self.model(x)
        
        
        loss, loss_items = self.criterion(y_pred, y, x[1], x[-1], attention_guide_decay=0)
        
        loss.backward()
        
        grad_norm = torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(), 1.0)    
            
        self.optimizer.step()
        self.scheduler.step()

        return loss_items

    def evaluate(self):
        validation_losses = []
        self.model.eval()

        for batch in self.eval_loader:
            x, y = self.model.parse_input(batch, self.device)

            with torch.no_grad():
                y_pred = self.model(x)

            loss, loss_items = self.criterion(y_pred, y, x[1], x[-1], attention_guide_decay=0) 
            validation_losses.append(loss_items)

        avg_validation_loss = np.mean(validation_losses, axis=0).tolist()

        return avg_validation_loss
    
    def global_mean(self, data_config):
        global_mean = torch.zeros(data_config['n_mel_channels']*data_config['n_frames_per_step'])
        total_frame = 0

        for batch in self.train_loader:
            _, _, mel_padded, _, output_lengths, _ = batch
            global_mean += mel_padded.sum(dim=(0, 2))
            total_frame += output_lengths.sum()
            
        global_mean = global_mean/total_frame

        if self.device.startswith('cuda'):
            global_mean = global_mean.to(self.device)

        return global_mean

    def sample(self):
        self.model.eval()
        for k in range(len(self.sample_text_inputs)):
            sample_text_ids = self.sample_text_inputs[k][:self.sample_text_lengths[k]][None,:]
            sample_mel = self.sample_mels[k][:, :self.sample_output_lengths[k]]
            
            with torch.no_grad():
                sample_outs = self.model.inference(sample_text_ids)
            
            plot_output(sample_outs, sample_mel, k, self.current_iter, self.log_dir) 

    def save_checkpoint(self):
        state = {
            'iter': self.current_iter,
            'best_eval_loss': self.best_eval_loss,
            'state_dict': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'scheduler': self.scheduler.state_dict(),
            'train_losses': self.train_losses,
            'eval_losses': self.eval_losses
        }    
        
        torch.save(state, os.path.join(self.log_dir, 'checkpoint.pt'))
        torch.save(self.model.state_dict(), os.path.join(self.log_dir, 'model.pt'))

    def load_checkpoint(self):
        state = torch.load(os.path.join(self.log_dir, 'checkpoint.pt'))
        self.current_iter = state['iter']
        self.best_eval_loss = state['best_eval_loss'] 
        self.model.load_state_dict(state['state_dict'])
        self.optimizer.load_state_dict(state['optimizer'])
        self.scheduler.load_state_dict(state['scheduler'])
        self.train_losses = state['train_losses']
        self.eval_losses = state['eval_losses']

        print('continue train from the checkpoint {}. current_iter: {}, best_eval_loss: {}'.format(os.path.join(self.log_dir, 'checkpoint'), self.current_iter, self.best_eval_loss))
