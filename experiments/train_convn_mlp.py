from pylearn2.config import yaml_parse
from time import gmtime, strftime
import os

__location__ = os.path.dirname(os.path.abspath(__file__))
yaml = open(os.path.join(__location__, 'convn_mlp.yaml'), 'r').read()
model = strftime('%Y-%m-%d_%H:%M', gmtime())

model_desc = '# Dropout model with max_norm constraints\n'

hyper_params = {
    'axes': '[\'b\', 0, 1, \'c\']',
    'batch_size' : 25,
    'input_size': 96,
    'nb_classes' : 63,

    'learning_rate' : 0.01,
    'lr_decay_factor': 0.1,

    'init_momentum' : 0.7,
    'final_momentum': .99,
    'save_path' : os.path.join(__location__, 'model_%s_live.pkl' % model),
    'save_path_best' : os.path.join(__location__, 'model_%s_best.pkl' % model),
    'output_channels_h1': 32,
    'output_channels_h2': 64,

    'dim_h3': 60,

    'pool_stride_h1': 2,
    'pool_stride_h2': 2,

    'pool_side_h1': 8,
    'pool_side_h2': 8,

    'kernel_side_h1': 6,
    'kernel_side_h2': 5,

    'max_kernel_norm_h1': 1.9,
    'max_kernel_norm_h2': 1.9,
    'max_col_norm_h3': 1.9365,
    'max_col_norm_y': 1.9365,

    'irange': .05,
    'istdev': .05,
    'sparse_init': 15,
}

yaml = yaml % (hyper_params)

with open(os.path.join(__location__, '%s_schema.yaml' % model), 'w') as schema:
    schema.write(model_desc)
    schema.write(yaml)

train = yaml_parse.load(yaml)
train.main_loop()
