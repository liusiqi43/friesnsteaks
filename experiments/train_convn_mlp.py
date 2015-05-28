from pylearn2.config import yaml_parse
from time import gmtime, strftime
import os

__location__ = os.path.dirname(os.path.abspath(__file__))
yaml = open(os.path.join(__location__, 'convn_mlp.yaml'), 'r').read()
model = strftime('%Y-%m-%d_%H:%M', gmtime())

model_desc = '# Dropout model with max_norm constraints\n'

hyper_params = {
    'axes': '[\'b\', 0, 1, \'c\']',
    'batch_size' : 50,
    'input_size': 36,
    'nb_classes' : 63,

    'learning_rate' : .01,
    'lr_decay_factor': .1,

    'init_momentum' : .5,
    'final_momentum': .7,
    'save_path' : os.path.join(__location__, 'model_%s_live.pkl' % model),
    'save_path_best' : os.path.join(__location__, 'model_%s_best.pkl' % model),
    'output_channels_h1': 32,
    'output_channels_h2': 64,

    'dim_h3': 200,
    'dim_h4': 200,

    'pool_stride_h1': 2,
    'pool_stride_h2': 2,

    'pool_side_h1': 4,
    'pool_side_h2': 4,

    'kernel_side_h1': 8,
    'kernel_side_h2': 8,

    'max_kernel_norm_h1': 1.9365,
    'max_kernel_norm_h2': 1.9365,
    'max_col_norm_h3': 1.9365,
    'max_col_norm_h4': 1.9365,
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
