train_config = {
        "num_iters": 500000,
        "learning_rate": 1e-4,
        "sigma": 1.0,
        "eval_steps": 2000,
        "batch_size": 12,
        "seed": 1234,
        "log_dir": "output/",
        "pretrained_url": '1yQWB9bMDckpncV2u-G-mmx3wCD048Ftt',
        'pretrained_md5': '436d8514f43f1cab2e494c6ff86cb538',
        'device':'cuda:0',
        'train_files':'train_files.txt',
        'test_files':'test_files.txt',
        'load_workers': 3,
    }

data_config = {
        "segment_length": 16000,
        "n_mel_channels": 80,
        "sampling_rate": 22050,
        "filter_length": 1024,
        "hop_length": 256,
        "win_length": 1024,
        "mel_fmin": 0.0,
        "mel_fmax": 8000.0
    }

waveglow_config =  {
        "n_mel_channels": 80,
        "n_flows": 12,
        "n_group": 8,
        "n_early_every": 4,
        "n_early_size": 2,
        "WaveNet_config": {
            "n_layers": 8,
            "n_channels": 256,
            "kernel_size": 3
        }
    }
