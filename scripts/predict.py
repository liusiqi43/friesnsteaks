import PIL, numpy as np, sys, theano
from PIL import Image
from pylearn2.utils import serial
from theano import tensor as T

def get_model_function(model_path):
    model = serial.load(model_path)
    X = model.get_input_space().make_theano_batch()
    Y = model.fprop(X)

    Y = T.argmax(Y, axis = 1)
    return theano.function([X], Y)

def get_np_img(img_path, show=False):
    img = Image.open(img_path)
    if show:
        img.show()
    data = np.zeros((1, img.size[0], img.size[1], 3))
    data[0] = np.asarray(img)
    return data



if __name__ == '__main__':
    f = get_model_function('../schemas/convolutional_network_best.pkl')

    while True:
        x = raw_input('Nom d\'image ? (q pour quitter)')
        if x == 'q':
            break
        else:
            img = get_np_img(x, True)
            print f(img)
