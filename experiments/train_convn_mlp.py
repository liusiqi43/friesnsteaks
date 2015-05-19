from pylearn2.config import yaml_parse
from time import gmtime, strftime


yaml = open("experiments/convn_mlp.yaml", 'r').read()

hyper_params = {
    'axes': "['b', 0, 1, 'c']",
    "batch_size" : 25,
    'input_size': 72,
    "img_width" : 72,
    "img_height" : 72,
    "nb_classes" : 74,
    "learning_rate" : 0.005,
    "save_path" : "experiments/model_%s_live.pkl" % strftime("%Y-%m-%d_%H:%M", gmtime()),
    "save_path_best" : "experiments/model_%s_best.pkl" % strftime("%Y-%m-%d_%H:%M", gmtime()),

    "output_channels_h1": 32,
    "output_channels_h2": 64,
    "output_channels_h3": 72,
    "output_channels_h4": 96,

    "dim_h5": 30,
    "dim_h6": 30,

    "pool_stride_h1": 2,
    "pool_stride_h2": 2,

    "pool_side_h1": 20,
    "pool_side_h2": 8,

    "kernel_side_h1": 6,
    "kernel_side_h2": 5,
    "kernel_side_h3": 3,
    "kernel_side_h4": 3,

    "sparse_init_h5": 15,
    "sparse_init_h6": 15,
}

yaml = yaml % (hyper_params)
train = yaml_parse.load(yaml)
train.main_loop()
