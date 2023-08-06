import argparse

from vietvoice.model.trainer import Trainer
from vietvoice.symbol import symbols, viphoneme_to_index
import vietvoice.config as cfg

def train(train_files, test_files, batch_size, device, resume):
    trainer = Trainer({**cfg.train_config, 'train_files': train_files, 'test_files':test_files, 'batch_size': batch_size, 'device':device}, 
            {**cfg.symbols_config, 'n_symbols':len(symbols)}, 
            cfg.data_config, 
            cfg.encoder_config, cfg.decoder_config, cfg.postnet_config,
            viphoneme_to_index
            )
    
    if resume:
        trainer.load_checkpoint()

    trainer.train()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_files', required=True, help='foo help')
    parser.add_argument('--test_files', required=True, help='foo help')
    parser.add_argument('--batch_size', default=30, type=int, help='foo help')
    parser.add_argument('--device', default='cuda:0', help='foo help')
    parser.add_argument('--resume', action='store_true')
   
    args = parser.parse_args()

    train(args.train_files, args.test_files, args.batch_size, args.device, args.resume) 
