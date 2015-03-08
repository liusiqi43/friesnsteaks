import theano
from pylearn2.config import yaml_parse

train = open('conv.yaml', 'r').read()
train_params = {'input_size': 48,}
train = train % (train_params)
train = yaml_parse.load(train)
train.main_loop()
