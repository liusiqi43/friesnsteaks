import sys
import os
import numpy as np
import pickle
import theano
from PIL import Image
from glob import glob
from pylearn2.utils import serial, string_utils

np.set_printoptions(precision=1)

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
    return np.asarray(img, dtype=theano.config.floatX)/127. - 1.

def get_np_imgs(img_paths):
    img = get_np_img(img_paths[0])

    data = np.zeros((len(img_paths), ) + img.shape, dtype=theano.config.floatX)
    for i, path in enumerate(img_paths):
        data[i] = get_np_img(path)
    return data

if __name__ == '__main__':
    f = get_model_function(sys.argv[1])
    # 'data/food100/output_resized_64/img_61_*.jpg'
    datapath = sys.argv[2]
    print 'Loading from: %s' % datapath

    images = get_np_imgs(glob(datapath))
    res = f(images)
    print res
    y = np.asarray([map(int, row+0.9) for row in res])

    label_names_pkl_path = os.path.join(string_utils.preprocess('${PYLEARN2_DATA_PATH}'), 'food100', 'label_names.pkl')
    label_names = None
    with open(label_names_pkl_path, 'rb') as label_names_pkl:
        label_names = pickle.load(label_names_pkl)

    class_count = [(label, np.count_nonzero(y[:,i])) for i, label in enumerate(label_names)]
    class_count.sort(lambda x, y: x[1] - y[1])
    print 'predicted count by class: '
    print class_count
