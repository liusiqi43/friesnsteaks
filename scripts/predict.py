import sys
import os
import numpy as np
import pickle
import theano
from PIL import Image
from glob import glob
from pylearn2.utils import serial

def get_model_function(model_path):
    model = serial.load(model_path)
    print model
    X = model.get_input_space().make_theano_batch()
    Y = model.fprop(X)

    # Y = tensor.argmax(Y, axis = 1)
    return theano.function([X], Y)

def get_np_img(img_path, show=False):
    img = Image.open(img_path)
    if show:
        img.show()
    data = np.zeros((1, img.size[0], img.size[1], 3))
    data[0] = np.asarray(img)
    return np.cast[theano.config.floatX](data)

if __name__ == '__main__':
    f = get_model_function(sys.argv[1])
    # 'data/food100/output_resized_64/img_61_*.jpg'
    datapath = sys.argv[2]
    print 'Loading from: %s' % datapath

    for example in glob(datapath):
        print example
        img = get_np_img(example, False)
        res = f(img)[0]
        print res
