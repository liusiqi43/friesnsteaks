import os
import logging
import sys
from theano import config
from glob import glob

import numpy
import random
import pickle

from PIL import Image

from pylearn2.datasets import cache, dense_design_matrix
from pylearn2.expr.preprocessing import global_contrast_normalize
from pylearn2.utils import contains_nan, serial, string_utils

from friesnsteaks.data.preprocessing.reclassify import reclassify


numpy.set_printoptions(threshold=numpy.nan)



class FOOD100(dense_design_matrix.DenseDesignMatrix):

    def __init__(self, which_set, input_size, axes):
        # make randomization deterministic
        random.seed(42)

        self.input_size = input_size
        image_to_labels, reclassified, _ = reclassify(which_set, input_size)

        self.img_shape = (input_size, input_size, 3)
        self.nclasses = len(reclassified)
        print '...nclasses = %d' % (self.nclasses)

        self.label_names = reclassified.keys()
        print '...label_names: \n%s' % self.label_names
        label_names_pkl = open(os.path.join( \
            string_utils.preprocess('${PYLEARN2_DATA_PATH}'), \
            'food100', 'label_names.pkl'), 'wb')
        pickle.dump(self.label_names, label_names_pkl)
        label_names_pkl.close()

        # prepare loading
        datapath = os.path.join(
            string_utils.preprocess('${PYLEARN2_DATA_PATH}'),
            'food100', 'output_%d' % input_size, which_set)

        images = image_to_labels.keys()
        random.shuffle(images)

        print '...generating %s set: %d examples' % (which_set, len(images))
        x = numpy.zeros((len(images), ) + self.img_shape, dtype=config.floatX)
        y = numpy.zeros((len(images), self.nclasses), dtype=config.floatX)

        for i, image in enumerate(images):
            img = Image.open(os.path.join(datapath, image))
            img = numpy.asarray(img, dtype=config.floatX)

            x[i] = img/127. - 1.

            for label in image_to_labels[image]:
                y[i][self.label_names.index(label)] = 1.

        # by default, we load images and store them as ('b', 0, 1, 'c')
        default_axes = ('b', 0, 1, 'c')
        dim_transpose = [axes.index(axis) for axis in default_axes]
        print '...from %s to %s with X.transpose(%s)' % (default_axes, axes, dim_transpose)
        x.transpose(dim_transpose)

        print '...%s set count by class' % which_set
        class_count = [(self.label_names[i], numpy.count_nonzero(y[:,i])) for i in xrange(y.shape[1])]
        class_count.sort(lambda x, y: x[1] - y[1])
        print class_count

        super(FOOD100, self).__init__(topo_view=x, y=y)
