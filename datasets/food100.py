import os
import logging
import sys
from theano import config

import numpy
import random
import pickle

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

    def __init__(self, which_set, input_size, axes, start=None,
                 stop=None):
        # make randomization deterministic
        random.seed(647)

        self.input_size = input_size
        image_to_labels, reclassified, instance_count = reclassify(input_size)
        ninstances = stop - start if start is not None else len(image_to_labels)
        ntrain = int(ninstances * .8)
        ntest = ninstances - ntrain
        print '...ninstances = %d, ntrain = %d, ntest = %d' % (ninstances, ntrain, ntest)

        self.img_shape = (input_size, input_size, 3)
        self.img_size = numpy.prod(self.img_shape)
        self.nclasses = len(reclassified)
        print '...nclasses = %d' % (self.nclasses)

        self.label_names = reclassified.keys()
        print '...label_names: \n%s' % self.label_names
        label_names_pkl = open(os.path.join( \
            string_utils.preprocess('${PYLEARN2_DATA_PATH}'), \
            'food100', 'label_names.pkl'), 'wb')
        pickle.dump(self.label_names, label_names_pkl)

        # prepare loading
        datapath = os.path.join(
            string_utils.preprocess('${PYLEARN2_DATA_PATH}'),
            'food100', 'output_resized_%d' % input_size)

        x = numpy.zeros((ninstances, ) + self.img_shape, dtype=config.floatX)
        # k-hot encoding
        y = numpy.zeros((ninstances, self.nclasses), dtype='int64')
        # y = numpy.zeros((ninstances), dtype='int64')

        # load data
        i = 0
        # randomize data
        images = image_to_labels.keys()
        random.shuffle(images)
        for image in images:
            img = Image.open(os.path.join(datapath, image))
            img = numpy.asarray(img, dtype=config.floatX)

            x[i] = img

            for label in image_to_labels[image]:
                y[i][self.label_names.index(label)] = 1
                # y[i] = self.label_names.index(label)
                break

            i = i+1
            if i == ninstances:
                break

        for sample in x:
            if numpy.all(sample == 0):
                raise Exception('Empty image sample')

        for sample in y:
            if numpy.all(sample == 0):
                raise Exception('Empty desired label')

        # process this data
        Xs = {'train': x[0:ntrain],
              'test': x[ntrain:(ntrain+ntest)]}

        # by default, we load images and store them as ('b', 0, 1, 'c')
        default_axes = ('b', 0, 1, 'c')
        dim_transpose = [axes.index(axis) for axis in default_axes]
        print '...from %s to %s with X.transpose(%s)' % (default_axes, axes, dim_transpose)
        for k, v in Xs.iteritems():
            Xs[k].transpose(dim_transpose)

        Ys = {'train': y[0:ntrain],
              'test': y[ntrain:(ntrain+ntest)]}

        X = Xs[which_set]
        y = Ys[which_set]

        print '...%s set count by class' % which_set
        class_count = [(self.label_names[i], numpy.count_nonzero(y[:,i])) for i in xrange(y.shape[1])]
        class_count.sort(lambda x, y: x[1] - y[1])
        print class_count

        print '...randomly printing three desired label examples...'
        for i in xrange(3):
            print random.choice(y[-10:])
        test_count = 10
        print '...randomly printing %d desired label examples...' % test_count
        for i in xrange(test_count):
            print random.choice(y)

        super(FOOD100, self).__init__(topo_view=X, axes=axes, y=y)

        assert not contains_nan(self.X)

    def get_test_set(self):
        return FOOD100(which_set='test', input_size=self.input_size, axes=axes)
