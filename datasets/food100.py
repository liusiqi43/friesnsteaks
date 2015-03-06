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


class FOOD100(dense_design_matrix.DenseDesignMatrix):

    """
    .. todo::

        WRITEME

    Parameters
    ----------
    which_set : str
        One of 'train', 'test'
    center : WRITEME
    rescale : WRITEME
    gcn : float, optional
        Multiplicative constant to use for global contrast normalization.
        No global contrast normalization is applied, if None
    start : WRITEME
    stop : WRITEME
    axes : WRITEME
    toronto_prepro : WRITEME
    preprocessor : WRITEME
    """

    def __init__(self, which_set, center=False, rescale=False, gcn=None,
                 start=None, stop=None, axes=('b', 0, 1, 'c'),
                 toronto_prepro = False, preprocessor = None):
        # note: there is no such thing as the cifar10 validation set;
        # pylearn1 defined one but really it should be user-configurable
        # (as it is here)

        self.axes = axes
        image_to_labels, reclassified, instance_count = reclassify()


        _logger.info('{} classes, with an average of {} examples per class.'.format(len(reclassified), sum(instance_count.values())/len(reclassified)))
        _logger.info('A total of {} examples.'.format(sum(instance_count.values())))
        ninstances = stop - start if start is not None else sum(instance_count.values())

        def dimshuffle(bc01):
            default = ('b', 0, 1, 'c')
            return bc01.transpose(*[default.index(axis) for axis in axes])

        # we define here:
        dtype = 'uint8'
        ntrain = ninstances * .8
        ntest = ninstances * .2
        print 'ntrain = %d, ntest = %f' % (ntrain, ntest)

        # we also expose the following details:
        self.img_shape = (128, 128, 3)
        self.img_size = numpy.prod(self.img_shape)
        self.n_classes = len(reclassified)

        self.label_names = reclassified.keys()
        print 'label_names:'
        print self.label_names
        label_names_pkl = open(os.path.join(string_utils.preprocess('${PYLEARN2_DATA_PATH}'), \
            'food100', 'output_resized', 'label_names.pkl'), 'wb')
        pickle.dump(self.label_names, label_names_pkl)

        # prepare loading
        datapath = os.path.join(
            string_utils.preprocess('${PYLEARN2_DATA_PATH}'),
            'food100', 'output_resized')

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
            img = Image.open(os.path.join(datapath, image)).convert('RGB')
            data[i] = numpy.asarray(img.rotate(90))
            for label in image_to_labels[image]:
                y[i][self.label_names.index(label)] = 1
            i = i+1
            if i == ninstances:
                break

        dimshuffle(data)

        for i in xrange(ninstances):
            x[i] = data[i].flatten('F')

        print x
        # process this data
        Xs = {'train': x[0:ntrain],
              'test': x[ntrain:ntrain+ntest]}

        Ys = {'train': y[0:ntrain],
              'test': y[ntrain:ntrain+ntest]}

        X = numpy.cast['float32'](Xs[which_set])
        y = Ys[which_set]

        if isinstance(y, list):
            y = numpy.asarray(y).astype(dtype)

        if center:
            X -= 127.5
        self.center = center

        if rescale:
            X /= 127.5
        self.rescale = rescale

        if toronto_prepro:
            assert not center
            assert not gcn
            X = X / 255.
            if which_set == 'test':
                other = FOOD100(which_set='train')
                oX = other.X
                oX /= 255.
                X = X - oX.mean(axis=0)
            else:
                X = X - X.mean(axis=0)
        self.toronto_prepro = toronto_prepro

        self.gcn = gcn
        if gcn is not None:
            gcn = float(gcn)
            X = global_contrast_normalize(X, scale=gcn)

        if which_set == 'test':
            assert X.shape[0] == ntest


        view_converter = dense_design_matrix.DefaultViewConverter(self.img_shape,
                                                                  self.axes)

        super(FOOD100, self).__init__(X=X, y=y, view_converter=view_converter,
                                      y_labels=self.n_classes)

        assert not contains_nan(self.X)

        if preprocessor:
            preprocessor.apply(self)

    def adjust_for_viewer(self, X):
        """
        .. todo::

        WRITEME
        """
        # assumes no preprocessing. need to make preprocessors mark the
        # new ranges
        rval = X.copy()

        # patch old pkl files
        if not hasattr(self, 'center'):
            self.center = False
        if not hasattr(self, 'rescale'):
            self.rescale = False
        if not hasattr(self, 'gcn'):
            self.gcn = False

        if self.gcn is not None:
            rval = X.copy()
            for i in xrange(rval.shape[0]):
                rval[i, :] /= numpy.abs(rval[i, :]).max()
            return rval

        if not self.center:
            rval -= 127.5

        if not self.rescale:
            rval /= 127.5

        rval = numpy.clip(rval, -1., 1.)

        return rval

    def __setstate__(self, state):
        super(FOOD100, self).__setstate__(state)
        # Patch old pkls
        if self.y is not None and self.y.ndim == 1:
            self.y = self.y.reshape((self.y.shape[0], 1))
        if 'y_labels' not in state:
            self.y_labels = 10

    def adjust_to_be_viewed_with(self, X, orig, per_example=False):
        """
        .. todo::

        WRITEME
        """
        # if the scale is set based on the data, display X oring the
        # scale determined by orig
        # assumes no preprocessing. need to make preprocessors mark
        # the new ranges
        rval = X.copy()

        # patch old pkl files
        if not hasattr(self, 'center'):
            self.center = False
        if not hasattr(self, 'rescale'):
            self.rescale = False
        if not hasattr(self, 'gcn'):
            self.gcn = False

        if self.gcn is not None:
            rval = X.copy()
            if per_example:
                for i in xrange(rval.shape[0]):
                    rval[i, :] /= numpy.abs(orig[i, :]).max()
                else:
                    rval /= numpy.abs(orig).max()
            rval = numpy.clip(rval, -1., 1.)
            return rval

        if not self.center:
            rval -= 127.5

        if not self.rescale:
            rval /= 127.5

        rval = numpy.clip(rval, -1., 1.)

        return rval

    def get_test_set(self):
        """
        .. todo::

        WRITEME
        """
        return FOOD100(which_set='test', center=self.center,
                       rescale=self.rescale, gcn=self.gcn,
                       toronto_prepro=self.toronto_prepro,
                       axes=self.axes)

