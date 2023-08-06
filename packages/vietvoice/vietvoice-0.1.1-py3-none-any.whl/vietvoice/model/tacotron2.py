import torch
import torch.nn as nn
import torch.nn.functional as F

from vietvoice.model.layers import Encoder, Decoder, Postnet
from vietvoice.utils.mask import get_mask_from_lengths, drop_frame

class Tacotron2Loss(nn.Module):
    def __init__(self):
        super(Tacotron2Loss, self).__init__()        
        self.attention_weights = 10
        
    @staticmethod
    def masked_l2_loss(out, target, mel_lengths):
        num_not_padded = mel_lengths.sum() * out.size(1)
        loss = F.mse_loss(out, target, reduction="sum")
        loss = loss / num_not_padded
    
        return loss
    
    @staticmethod
    def masked_alignment_loss(alignment, guided_alignment, text_lengths, mel_lengths):
        num_not_padded = torch.sum(text_lengths*mel_lengths)
        loss = alignment*guided_alignment
        loss = torch.sum(loss)/num_not_padded
        
        return loss
    
    def forward(self, model_outputs, targets, text_lengths, mel_lengths, attention_guide_decay):
        mel_targets, gate_targets, guided_alignment = targets
        
        mel_outputs, mel_outputs_postnet, gate_outputs, alignment = model_outputs
        
        mel_loss = self.masked_l2_loss(mel_outputs, mel_targets, mel_lengths) + self.masked_l2_loss(mel_outputs_postnet, mel_targets, mel_lengths)
    
        gate_loss = nn.BCEWithLogitsLoss()(gate_outputs, gate_targets)
        
        alignment_loss = self.masked_alignment_loss(alignment, guided_alignment, text_lengths, mel_lengths)
        alignment_loss = attention_guide_decay*self.attention_weights*alignment_loss
        
        total_loss = mel_loss + gate_loss + alignment_loss
                
        return total_loss, (total_loss.item(), mel_loss.item(), gate_loss.item(), alignment_loss.item())

class Tacotron2(nn.Module):
    def __init__(self, n_mel_channels, n_frames_per_step, drop_frame_rate, global_mean, n_symbols, symbols_embedding_dim, 
                 encoder_config, decoder_config, postnet_config):
        super(Tacotron2, self).__init__()
        
        self.n_mel_channels = n_mel_channels
        self.n_frames_per_step = n_frames_per_step
        self.drop_frame_rate = drop_frame_rate
        self.global_mean = global_mean
        
        self.embedding = nn.Embedding(n_symbols, symbols_embedding_dim, padding_idx=0)
        self.encoder = Encoder(**encoder_config)
        self.decoder = Decoder(n_mel_channels=n_mel_channels*n_frames_per_step,
                               **decoder_config)
        self.postnet = Postnet(n_mel_channels=n_mel_channels*n_frames_per_step,
                               **postnet_config)
    
    def parse_input(self, batch, device):
        text_padded, input_lengths, mel_padded, gate_padded, output_lengths, guided_alignments  = batch
        
        text_padded = text_padded.to(device)
        input_lengths = input_lengths.to(device)
        mel_padded = mel_padded.to(device)
        gate_padded = gate_padded.to(device)
        output_lengths = output_lengths.to(device)
        guided_alignments = guided_alignments.to(device)
        
        X = text_padded, input_lengths, mel_padded, output_lengths
        y = mel_padded, gate_padded, guided_alignments
        
        return  X, y
    
    def transform_output(self, mel_outputs, mel_outputs_postnet, gate_outputs, alignments, text_lengths=None, output_lengths=None):
        if output_lengths is not None:
            mask_t_in = get_mask_from_lengths(text_lengths)
            mask_t_out = get_mask_from_lengths(output_lengths)
            mask_alignments = mask_t_out.unsqueeze(-1)*mask_t_in.unsqueeze(1)
            
            mask_t_in = ~mask_t_in
            mask_t_out = ~mask_t_out
            mask_alignments = ~mask_alignments
            
            mask_output = mask_t_out.expand(self.n_mel_channels*self.n_frames_per_step, -1, -1)
            mask_output = mask_output.permute(1, 0, 2) # BxHxT
            
            mel_outputs.masked_fill_(mask_output, 0.0)
            mel_outputs_postnet.masked_fill_(mask_output, 0.0)
            gate_outputs.masked_fill_(mask_output[:, 0, :], 1e3)
            alignments.masked_fill_(mask_alignments, 0.0)
            
        return mel_outputs, mel_outputs_postnet, gate_outputs, alignments
    
    def decouple_frames(self, mel_outputs):
        batch_size = mel_outputs.size(0)
        
        mel_outputs = mel_outputs.transpose(1, 2)
        mel_outputs = mel_outputs.reshape(batch_size, -1, self.n_mel_channels)
        mel_outputs = mel_outputs.transpose(1, 2)
        
        return mel_outputs
    
    def forward(self, inputs):
        text_inputs, text_lengths, mels, output_lengths = inputs
        
#         if self.global_mean != None and self.drop_frame_rate > 0 and self.training:
#             mels = drop_frame(mels, self.global_mean, output_lengths, self.drop_frame_rate)
         
        embedded_inputs = self.embedding(text_inputs)
        embedded_inputs = embedded_inputs.transpose(1, 2) # BxHxT
                
        encoder_outputs = self.encoder(embedded_inputs, text_lengths)
        
        mel_outputs, gate_outputs, alignments = self.decoder(encoder_outputs, mels, memory_lengths=text_lengths)
        
        mel_outputs_postnet = self.postnet(mel_outputs)
        mel_outputs_postnet = mel_outputs_postnet + mel_outputs
        
        outputs = self.transform_output(mel_outputs, mel_outputs_postnet, gate_outputs, alignments, text_lengths, output_lengths)
        
        return outputs
    
    def inference(self, inputs):
        """
        inputs: tensor of text idx
        """
        
        embedded_inputs = self.embedding(inputs).transpose(1, 2)
        encoder_outputs = self.encoder.inference(embedded_inputs)
        
        mel_outputs, gate_outputs, alignments = self.decoder.inference(encoder_outputs)
        
        mel_outputs_postnet = self.postnet(mel_outputs)
        mel_outputs_postnet = mel_outputs_postnet + mel_outputs
        
        outputs = self.transform_output(mel_outputs, mel_outputs_postnet, gate_outputs, alignments)
        return outputs
