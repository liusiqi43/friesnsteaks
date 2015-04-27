import numpy as np
import pickle
import sys
import theano
from PIL import Image
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
    label_names = pickle.load(open('../data/food100/label_names.pkl', 'rb'))

    while True:
        x = raw_input('Nom d\'image ? (q pour quitter) ')
        if x == 'q':
            break
        else:
            img = get_np_img(x, True)
            res = f(img)[0]
            print res
            print ','.join([label_names[i] for i in xrange(len(res)) if res[i] > 0])
