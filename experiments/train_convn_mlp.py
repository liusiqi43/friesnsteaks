from pylearn2.config import yaml_parse
from time import gmtime, strftime


yaml = open("experiments/convn_mlp.yaml", 'r').read()

hyper_params = {
    'axes': "['b', 0, 1, 'c']",
    "batch_size" : 25,
    'input_size': 96,
    "img_width" : 96,
    "img_height" : 96,
    "nb_classes" : 74,
    "learning_rate" : 0.005,
    "save_path" : "experiments/model_%s_live.pkl" % strftime("%Y-%m-%d_%H:%M", gmtime()),
    "save_path_best" : "experiments/model_%s_best.pkl" % strftime("%Y-%m-%d_%H:%M", gmtime()),

    "output_channels_h1": 48,
    "output_channels_h2": 96,
    "output_channels_h3": 128,
    "output_channels_h4": 128,
    "output_channels_h5": 128,
    "output_channels_h6": 74,

    "pool_stride_h1": 2,
    "pool_stride_h3": 2,
    "pool_stride_h5": 2,

    "pool_side_h1": 2,
    "pool_side_h3": 2,
    "pool_side_h5": 2,

    "kernel_side_h1": 5,
    "kernel_side_h2": 7,
    "kernel_side_h3": 5,
    "kernel_side_h4": 5,
    "kernel_side_h5": 3,
    "kernel_side_h6": 6,

    "weight_decay_h2": 0.00005,
    "weight_decay_h3": 0.00005,
    "weight_decay_h4": 0.00005,
    "weight_decay_h5": 0.00005,
    "weight_decay_h6": 0.00005,
    "weight_decay_y": 0.00005,
}

yaml = yaml % (hyper_params)
train = yaml_parse.load(yaml)
train.main_loop()
