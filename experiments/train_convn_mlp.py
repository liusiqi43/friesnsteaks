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

    "output_channels_h2": 12,
    "output_channels_h3": 12,

    "pool_stride_h2": 1,
    "pool_stride_h3": 1,

    "pool_side_h2": 3,
    "pool_side_h3": 3,

    "kernel_side_h2": 8,
    "kernel_side_h3": 8,

    "dim_h4": 30,
    "dim_h5": 30,
    "dim_h6": 30,

    "sparse_init_h4": 2,
    "sparse_init_h5": 2,
    "sparse_init_h6": 2,

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
