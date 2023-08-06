import torch
from scipy.io import wavfile
import math
from numba import jit
import numpy as np
import os

from vietvoice.stft import TacotronSTFT

MAX_WAV_VALUE = 32768.0

def load_wav_to_torch(full_path):
    sampling_rate, data = wavfile.read(full_path)
    return torch.FloatTensor(data.astype(np.float32)), sampling_rate


def load_filepaths_and_text(filename, split="|"):
    with open(filename, encoding='utf-8') as f:
        filepaths_and_text = [line.strip().split(split) for line in f]
    return filepaths_and_text

@jit
def get_guided_alignment(text_length, mel_length):
    w = np.zeros((mel_length, text_length))
    
    for i in range(mel_length):
        for j in range(text_length):
            w[i, j] = 1 - math.exp(-((i/mel_length - j/text_length)**2)/(2*0.2**2))
    
    return w

def save_mel(fin, out, data_config):
    stft = TacotronSTFT(**data_config)
    
    os.makedirs(out, exist_ok=True)

    filenames = load_filepaths_and_text(fin)

    for item in filenames:
        audiopath = item[0]
        audio, sampling_rate = load_wav_to_torch(audiopath)
        audio_norm = audio/MAX_WAV_VALUE
        audio_norm = audio_norm.unsqueeze(0)
        mel = stft.mel_spectrogram(audio_norm)
        mel = mel.squeeze(0).numpy()

        np.save('{}/{}.npy'.format(out, os.path.basename(audiopath)), mel)

class TextMelCollate():
    
    def __init__(self):
        pass
    
    def __call__(self, batch):
        
        batch_size = len(batch)
        text_lengths = [len(text) for text, _, _ in batch]
        
        input_lengths, ids_sorted_descreasing = torch.sort(
            torch.LongTensor(text_lengths),
            dim=0,
            descending=True
        )
    
        max_input_length = input_lengths[0]
        
        text_padded = torch.LongTensor(batch_size, max_input_length).zero_()
        
        for i in range(batch_size):
            text = batch[ids_sorted_descreasing[i]][0]
            text_padded[i, :len(text)] = text
        
        num_mels = batch[0][1].size(0)
        
        max_target_len = max([x[1].size(1) for x in batch])            
            
        mel_padded = torch.FloatTensor(batch_size, num_mels, max_target_len).zero_()        
        gate_padded = torch.FloatTensor(batch_size, max_target_len).zero_()
        output_lengths = torch.LongTensor(batch_size)
        
        for i in range(batch_size):
            mel = batch[ids_sorted_descreasing[i]][1]
            mel_padded[i, :, :mel.size(1)] = mel
            gate_padded[i, mel.size(1) - 1: ] = 1
            output_lengths[i] = mel.size(1)
        
        guided_alignments = torch.zeros(batch_size, max_target_len, max_input_length)
        for i in range(batch_size):
            alignment = batch[ids_sorted_descreasing[i]][2]
            guided_alignments[i,:alignment.size(0),:alignment.size(1)] = alignment
        
        return text_padded, input_lengths, mel_padded, gate_padded, output_lengths, guided_alignments
    
class TextMelLoader(torch.utils.data.Dataset):
    
    def __init__(self, dataset, text_to_index_fn, n_frames_per_step, sampling_rate, 
                 filter_length, hop_length, win_length, n_mel_channels, 
                 mel_fmin, mel_fmax, precomputed_mels=None):
        
        self.dataset = load_filepaths_and_text(dataset)
        self.text_to_index_fn = text_to_index_fn
        self.n_frames_per_step = n_frames_per_step
        
        self.precomputed_mels = precomputed_mels
        
        self.stft = TacotronSTFT(filter_length=filter_length, hop_length=hop_length, 
                         win_length=win_length, n_mel_channels=n_mel_channels, 
                         sampling_rate=sampling_rate, 
                         mel_fmin=mel_fmin, mel_fmax=mel_fmax)
            
    def __len__(self):
        return len(self.dataset)
    
    def get_mel_text(self, audiopath_and_text):
        audiopath, text = audiopath_and_text[0], audiopath_and_text[1]
        
        mel = self.get_mel(audiopath)
        text = self.get_text(text)
        
        return (text, mel)
    
    def get_text(self, text):
        text = self.text_to_index_fn(text)        
    
        text = torch.IntTensor(text)
        
        return text
    
    def get_mel(self, audiopath):
        audio, sampling_rate = load_wav_to_torch(audiopath)
        audio_norm = audio/MAX_WAV_VALUE
        audio_norm = audio_norm.unsqueeze(0)
        mel = self.stft.mel_spectrogram(audio_norm)
        mel = mel.squeeze(0)
        
        return mel
            
        
    def __getitem__(self, index):
        audiopath_and_text = self.dataset[index]
        audiopath, text = audiopath_and_text[0], audiopath_and_text[1]
        
        text = self.get_text(text)
        
        if self.precomputed_mels is None:
            mel = self.get_mel(audiopath)
        else:
            mel_fname = os.path.basename(audiopath)
            mel = torch.from_numpy(np.load('{}/{}.npy'.format(self.precomputed_mels, mel_fname)))
        
        if self.n_frames_per_step > 1:
            mel_length = mel.size(1)
            if mel_length % self.n_frames_per_step != 0:
                mel_length = (mel_length//self.n_frames_per_step)*self.n_frames_per_step
            new_mel = mel[:, :mel_length]
            
            mel = new_mel.transpose(0, 1)
            mel = mel.reshape(mel_length//self.n_frames_per_step, -1)
            mel = mel.transpose(0, 1)
            
        guided_alignment = get_guided_alignment(text.size(0), mel.size(1))
        guided_alignment = torch.from_numpy(guided_alignment)
        
        return text, mel, guided_alignment
