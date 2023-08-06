import numpy as np
import torch

from vietvoice.model.tacotron2 import Tacotron2
import vietvoice.config as cfg

class Predictor():
    def __init__(self, symbols_config, data_config, encoder_config, decoder_config, postnet_config, text_to_index_fn, weights, device):
        self.device = device
        self.text_to_index_fn = text_to_index_fn
        self.n_mel_channels = data_config['n_mel_channels']

        self.model = Tacotron2(n_mel_channels=self.n_mel_channels,
                  n_frames_per_step=data_config['n_frames_per_step'],
                  drop_frame_rate=0,
                  global_mean=None,
                  **symbols_config,
                  encoder_config=encoder_config,
                  decoder_config=decoder_config,
                  postnet_config=postnet_config)
        self.model.eval()
        self.model.load_state_dict(torch.load(weights))
        
        if self.device.startswith('cuda'):
            self.model = self.model.cuda()

    def predict(self, text):
        indices = self.text_to_index_fn(text)

        indices = torch.IntTensor(indices).reshape(1, -1)
        if self.device.startswith('cuda'):
            indices = indices.to(self.device)
        
        with torch.no_grad():
            outputs = self.model.inference(indices)
        
        mel = outputs[1].cpu().numpy()[0]
        # decouple for multi-frame per step
        mel = mel.T.reshape(-1, self.n_mel_channels).T

        return mel

