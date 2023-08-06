import numpy as np
import torch

import matplotlib.pyplot as plt
from matplotlib import figure

def plot_loss(losses, figname, log_dir):
    fig = figure.Figure(figsize=(20,12), tight_layout=True)
    axs = fig.subplots(4,1)
    for axis_idx, loss_name in enumerate(['total loss', 'mel loss', 'gate loss', 'alignment loss']):
        axs[axis_idx].plot([item[0] for item in losses], [item[axis_idx+1] for item in losses])
        axs[axis_idx].set_title(loss_name)
    
    fig.savefig('{}/{}.jpg'.format(log_dir, figname))
    plt.close()

def plot_output(model_outputs, sample_mel, sample_idx, i, log_dir):
    fig = figure.Figure(figsize=(20,12), tight_layout=True)
    axs = fig.subplots(4,1, gridspec_kw={'height_ratios': [3, 1, 2, 2]})

    # attention
    axs[0].imshow(model_outputs[-1][0].cpu().numpy().T, aspect='auto', origin='bottom', 
              interpolation='none')
    axs[0].set_title('attention')
    # gate
    axs[1].plot(torch.sigmoid(model_outputs[-2][0]).cpu().numpy())
    axs[1].set_title('gate')
    # mels
    mel_postnet_prediction = model_outputs[1][0].cpu().numpy()
    axs[2].imshow(mel_postnet_prediction, aspect='auto', origin='bottom', 
               interpolation='none')
    axs[2].set_title('mels')
    
    axs[3].imshow(sample_mel.cpu().numpy(), aspect='auto', origin='bottom', 
               interpolation='none')
    axs[3].set_title('target')
    
    fig.savefig('{}/{:03d}_{:06d}.jpg'.format(log_dir, sample_idx, i))
    plt.close()
    
    np.save('{}/mel_{:03d}_{:06d}.npy'.format(log_dir, sample_idx, i), mel_postnet_prediction)
