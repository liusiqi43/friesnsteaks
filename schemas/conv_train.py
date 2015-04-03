import theano
from pylearn2.config import yaml_parse
train = open('conv.yaml', 'r').read()

input_size = 48
nvis = input_size * input_size * 3
axes = ['b', 0, 1, 'c']

train_params = {
    'input_size': input_size,
    'nvis': nvis,
    'axes': axes
}

train = train % (train_params)
train = yaml_parse.load(train)
train.main_loop()
