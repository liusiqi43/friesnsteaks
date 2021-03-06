from pylearn2.config import yaml_parse
from time import gmtime, strftime
import os

__location__ = os.path.dirname(os.path.abspath(__file__))
yaml = open(os.path.join(__location__, 'convn_mlp.yaml'), 'r').read()
model = strftime('%Y-%m-%d_%H:%M', gmtime())

model_desc = '#Architecture inspired by stanford guide with dropout\n'

hyper_params = {
    'axes': '["b", 0, 1, "c"]',
    'batch_size' : 50,
    'input_size': 32,
    'nb_classes' : 63,

    'learning_rate' : .01,
    'lr_decay_factor': .1,

    'init_momentum' : .5,
    'final_momentum': .7,
    'save_path' : os.path.join(__location__, 'model_%s_live.pkl' % model),
    'save_path_best' : os.path.join(__location__, 'model_%s_best.pkl' % model),

    'output_channels_h0': 32,
    'output_channels_h1': 64,

    'dim_h2': 200,
    'dim_h3': 200,

    'kernel_side_h0': 8,
    'kernel_side_conv': 8,

    'pool_side_conv': 4,
    'pool_stride_conv': 2,

    'max_norm': 1.9365,

    'irange': .05,

    'weight_decay': .005,
}

yaml = yaml % (hyper_params)

with open(os.path.join(__location__, '%s_schema.yaml' % model), 'w') as schema:
    schema.write(model_desc)
    schema.write(yaml)

train = yaml_parse.load(yaml)
train.main_loop()
