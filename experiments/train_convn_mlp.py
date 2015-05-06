from pylearn2.config import yaml_parse


yaml = open("experiments/convn_mlp.yaml", 'r').read()

hyper_params = {
    'axes': "['b', 0, 1, 'c']",
    "batch_size" : 100,
    'input_size': 64,
    "img_width" : 64,
    "img_height" : 64,
    "nb_classes" : 2,
    "weight_decay_y": 0.0,
    "learning_rate" : 0.01,
    "max_epochs": 100 ,
    "save_path" : "experiments/model_live.pkl",
    "save_path_best" : "experiments/model_best.pkl",
    # "output_channels_h2": 6,
    # "kernel_side_h2": 3,
    # "pool_side_h2": 5,
    # "pool_stride_h2": 5,
}

yaml = yaml % (hyper_params)
train = yaml_parse.load(yaml)
train.main_loop()
