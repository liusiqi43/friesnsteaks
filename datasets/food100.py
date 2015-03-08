"""
.. todo::

    WRITEME
"""
import os
import logging

import numpy
import random
import pickle
from theano.compat.six.moves import xrange

from PIL import Image

from pylearn2.datasets import cache, dense_design_matrix
from pylearn2.expr.preprocessing import global_contrast_normalize
from pylearn2.utils import contains_nan
from pylearn2.utils import serial
from pylearn2.utils import string_utils

from friesnsteaks.data.preprocessing.reclassify import reclassify


_logger = logging.getLogger(__name__)
numpy.set_printoptions(threshold=numpy.nan)



class FOOD100(dense_design_matrix.DenseDesignMatrix):

    def __init__(self, which_set, input_size, start=None,
                 stop=None, axes=('b', 0, 1, 'c')):
        self.axes = axes
        self.input_size = input_size
        image_to_labels, reclassified, instance_count = reclassify()

        _logger.info('{} classes, with an average of {} examples per class.'.format(len(reclassified), sum(instance_count.values())/len(reclassified)))
        _logger.info('A total of {} examples.'.format(sum(instance_count.values())))
        ninstances = stop - start if start is not None else sum(instance_count.values())

        dtype = 'uint8'
        ntrain = ninstances * .8
        ntest = ninstances * .2
        print 'ntrain = %d, ntest = %f' % (ntrain, ntest)

        self.img_shape = (input_size, input_size, 3)
        self.img_size = numpy.prod(self.img_shape)
        self.n_classes = len(reclassified)

        self.label_names = reclassified.keys()
        print 'label_names:'
        print self.label_names
        label_names_pkl = open(os.path.join(string_utils.preprocess('${PYLEARN2_DATA_PATH}'), \
            'food100', 'label_names.pkl'), 'wb')
        pickle.dump(self.label_names, label_names_pkl)

        # prepare loading
        datapath = os.path.join(
            string_utils.preprocess('${PYLEARN2_DATA_PATH}'),
            'food100', 'output_resized_%d' % input_size)

        # k-hot encoding
        x = numpy.zeros((ninstances, self.img_size), dtype=dtype)
        y = numpy.zeros((ninstances, self.n_classes), dtype=dtype)

        data = numpy.zeros((ninstances, self.img_shape[0], \
                            self.img_shape[1], self.img_shape[2]), dtype=dtype)

        # load data
        i = 0
        # randomize data
        images = image_to_labels.keys()
        random.shuffle(images)
        for image in images:
            img = Image.open(os.path.join(datapath, image))
            x[i] = numpy.asarray(img).flatten('F')
            for label in image_to_labels[image]:
                y[i][self.label_names.index(label)] = 1
                break
            i = i+1
            if i == ninstances:
                break

        # process this data
        Xs = {'train': x[0:ntrain],
              'test': x[ntrain:ntrain+ntest]}

        Ys = {'train': y[0:ntrain],
              'test': y[ntrain:ntrain+ntest]}

        X = numpy.cast['float32'](Xs[which_set])
        y = Ys[which_set]

        if isinstance(y, list):
            y = numpy.asarray(y).astype(dtype)

        if which_set == 'test':
            assert X.shape[0] == ntest

        view_converter = dense_design_matrix.DefaultViewConverter(self.img_shape,
                                                                  self.axes)

        super(FOOD100, self).__init__(X=X, y=y, view_converter=view_converter,
                                      y_labels=self.n_classes)

        assert not contains_nan(self.X)

    def get_test_set(self):
        return FOOD100(which_set='test', input_size=self.input_size, axes=self.axes)
