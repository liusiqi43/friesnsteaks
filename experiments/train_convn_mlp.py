from pylearn2.config import yaml_parse
from time import gmtime, strftime

# L2-regularized model

yaml = open('experiments/convn_mlp.yaml', 'r').read()

hyper_params = {
    'axes': '[\'b\', 0, 1, \'c\']',
    'batch_size' : 25,
    'input_size': 96,
    'nb_classes' : 63,
    'learning_rate' : 0.05,
    'lr_decay_factor': 0.1,
    'init_momentum' : 0.7,
    'final_momentum': .99,
    'save_path' : 'experiments/model_%s_live.pkl' % strftime('%Y-%m-%d_%H:%M', gmtime()),
    'save_path_best' : 'experiments/model_%s_best.pkl' % strftime('%Y-%m-%d_%H:%M', gmtime()),

    'output_channels_h1': 32,
    'output_channels_h2': 64,

    'dim_h3': 100,

    'pool_stride_h1': 2,
    'pool_stride_h2': 2,

    'pool_side_h1': 8,
    'pool_side_h2': 8,

    'kernel_side_h1': 5,
    'kernel_side_h2': 5,

    'max_kernel_norm_h1': 1.9,
    'max_kernel_norm_h2': 1.9,
    'max_col_norm_h3': 1.9365,
    'max_col_norm_y': 1.9365
}

yaml = yaml % (hyper_params)
train = yaml_parse.load(yaml)
train.main_loop()
