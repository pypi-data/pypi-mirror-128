
train_config = {
        "num_iters": 200000,
        "learning_rate": 5e-4,
        "eval_steps": 2000,
        "batch_size": 30,
        "log_dir": "output/",
        "device":'cuda:0',
        "precomputed_mels":"mels/",
        "warmup_steps":50000,
        "train_files":"train_files.txt",
        "test_files": "test_files.txt",
        "drop_frame_rate":0.2,
        "pretrained_url":"1sdo0mwL7pEtXFp_EZiLE2H3DTNDo2Yb_",
        "pretrained_md5":"47727ea0a3df6c966f445c8502943802"
    }

data_config = {
        "n_mel_channels": 80,
        "n_frames_per_step":1,
        "sampling_rate": 22050,
        "filter_length": 1024,
        "hop_length": 256,
        "win_length": 1024,
        "mel_fmin": 0.0,
        "mel_fmax": 8000.0
    }

symbols_config = {
    "symbols_embedding_dim": 512
}

encoder_config = {
    "n_convolutions": 3,  
    "kernel_size": 5,
    "embedding_dim": 512
}

decoder_config = {
    "encoder_embedding_dim": encoder_config['embedding_dim'], 
    "attention_rnn_dim": 1024, 
    "decoder_rnn_dim": 1024, 
    "prenet_dim": 256, 
    "max_decoder_steps": 2000, 
    "gate_threshold": 0.5, 
    "p_attention_dropout": 0.1,
    "p_decoder_dropout": 0.1,
    "attention_config": {
        "attention_location_n_filters": 32,
        "attention_location_kernel_size": 31,
        "attention_dim": 128,
        
    }
}

postnet_config = {
    "n_convolutions": 5, 
    "embedding_dim": 512, 
    "kernel_size": 5
}
