import torch

def get_mask_from_lengths(lengths):
    max_length = torch.max(lengths).item()
    ids = torch.arange(0, max_length, device=lengths.device)
    mask = (ids < lengths.unsqueeze(1)).bool()

    return mask

def get_drop_frame_mask_from_lengths(lengths, drop_frame_rate):
    batch_size = lengths.size(0)
    max_len = torch.max(lengths).item()


#     mask = get_mask_from_lengths(lengths)
    ##

    max_length = torch.max(lengths).item()
    ids = torch.arange(0, max_length, device=lengths.device)
    mask = (ids < lengths.unsqueeze(1) -5 ).bool()

    ###

    drop_mask = torch.empty((batch_size, max_len), device=lengths.device).uniform_(0., 1.) < drop_frame_rate

    drop_mask = drop_mask.float() * mask

    return drop_mask

def drop_frame(mels, global_mean, mel_lengths, drop_frame_rate):
    drop_mask = get_drop_frame_mask_from_lengths(mel_lengths, drop_frame_rate)
    drop_mask = drop_mask.unsqueeze(1)
    global_mean = global_mean[None,:,None]

    dropped_mels = mels*(1 - drop_mask) + global_mean*drop_mask

    return dropped_mels
