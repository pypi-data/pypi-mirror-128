import numpy as np
import torch

from vietvoice.model.tacotron2 import Tacotron2
from vietvoice.symbol import Symbol

class Predictor():
    def __init__(self, config, weights, device):

        symbols_config = config['symbols_config']
        data_config = config['data_config']
        encoder_config = config['encoder_config']
        decoder_config = config['decoder_config']
        postnet_config = config['postnet_config']

        self.device = device
        self.n_mel_channels = data_config['n_mel_channels']
        
        self.symbols = Symbol(**symbols_config)

        self.model = Tacotron2(n_mel_channels=self.n_mel_channels,
                  n_frames_per_step=data_config['n_frames_per_step'],
                  drop_frame_rate=0,
                  global_mean=None,
                  n_symbols = len(self.symbols),
                  symbols_embedding_dim= symbols_config['symbols_embedding_dim'],
                  encoder_config=encoder_config,
                  decoder_config=decoder_config,
                  postnet_config=postnet_config)
        self.model.eval()
        self.model.load_state_dict(torch.load(weights))
        
        if self.device.startswith('cuda'):
            self.model = self.model.to(self.device)

    def predict(self, text):
        indices = self.symbols(text)

        indices = torch.IntTensor(indices).reshape(1, -1)
        if self.device.startswith('cuda'):
            indices = indices.to(self.device)
        
        with torch.no_grad():
            outputs = self.model.inference(indices)
        
        mel = outputs[1].cpu().numpy()[0]
        # decouple for multi-frame per step
        mel = mel.T.reshape(-1, self.n_mel_channels).T

        return mel

