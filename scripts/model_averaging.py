import sys
import os
import numpy as np
import pickle
import csv
import theano
import matplotlib.pyplot as plt

from PIL import Image
from glob import glob
from pylearn2.utils import serial, string_utils
from sklearn.metrics import confusion_matrix
from datasets.reclassify import get_classes, get_mapping
from scripts.analysis import get_np_img, get_np_imgs, get_confusion_matrix, get_misclass, get_model_function, is_included, save_report

np.set_printoptions(threshold=np.nan)

def get_voters(models_path):
    voters = glob(models_path)
    voters.sort()
    return voters

def get_voted_confusion_matrix(n_classes, voters, confidence_matrix, test_set, batch):
    result = np.zeros((n_classes, n_classes), dtype=float)
    imageShape = get_np_img(test_set[0]).shape
    batch_size = len(test_set)/batch

    fs = [get_model_function(voter) for voter in voters]

    print 'processing %d batches ' % batch,
    for i in xrange(batch):
        print '.',
        images, ytrue = get_np_imgs(test_set[i*batch_size:(i+1)*batch_size], imageShape, id_to_class, class_to_superclass, class_to_label)

        # FxN_IMAGESxN_CLASSES
        res = np.zeros((len(fs), len(images), n_classes))
        for i, f in enumerate(fs):
            res[i] = f(images)

        # transpose to N_IMAGESxFxN_CLASSES
        # for each image, we can do N_CLASSESxF dot FxN_CLASSES to get weighted prediction per image
        res = np.transpose(res, (1, 0, 2))

        weighted_res = np.zeros((len(images), n_classes))
        for i, mat in enumerate(res):
            # dot product and then sum by column
            weighted_res[i] = np.sum(mat * confidence_matrix, axis=0)

        ypred = np.argmax(weighted_res, axis=1)
        cm = confusion_matrix(ytrue, ypred, range(n_classes)).astype(float)
        result += cm
    print '.'

    # column major normalization.
    #         ytrue
    #       ----------
    #       |        |
    # ypred |        |
    #       |        |
    #       ----------

    return result

if __name__ == '__main__':

    if len(sys.argv) < 5:
        print 'Usage: analysis.py <path/to/voter_models> <path/to/valid_images> <path/to/test_images> <batch>'
        sys.exit(-1)

    models_path = sys.argv[1]
    # 'data/food100/output_resized_64/img_61_*.jpg'
    valid_path = sys.argv[2]
    test_path = sys.argv[3]
    batch = int(sys.argv[4])

    class_to_id = get_classes()
    id_to_class = {v: k for k, v in class_to_id.items()}
    class_to_superclass = get_mapping()

    label_names_pkl_path = os.path.join(string_utils.preprocess('${PYLEARN2_DATA_PATH}'), 'food100', 'label_names.pkl')
    label_names_pkl = open(label_names_pkl_path, 'rb')
    label_names = pickle.load(label_names_pkl)
    class_to_label = {l : i for i, l in enumerate(label_names)}
    label_names_pkl.close()

    print 'Loading valid set from: %s' % valid_path
    valid_set = [img for img in glob(valid_path) if is_included(img, class_to_superclass, id_to_class)]

    voters = get_voters(models_path)
    confidence_matrix = np.zeros((len(voters), len(label_names)), dtype=float)
    for i, voter in enumerate(voters):
        cm = get_confusion_matrix(len(label_names), id_to_class, class_to_superclass, class_to_label, valid_set, voter, batch)
        print 'model#%d... misclass rate: %f' % (i, get_misclass(cm))
        cm /= np.sum(cm, axis=0)
        confidence_matrix[i] = cm.diagonal()

    # column major normalization, or try softmax?
    confidence_matrix /= np.sum(confidence_matrix, axis=0)
    # equal votes if none know the answer
    confidence_matrix[np.isnan(confidence_matrix)] = 1./len(voters)

    print 'Loading test set from: %s' % test_path
    test_set = [img for img in glob(test_path) if is_included(img, class_to_superclass, id_to_class)]
    vcm = get_voted_confusion_matrix(len(label_names), voters, confidence_matrix, test_set, batch)
    print 'voted model... misclass rate: %f' % get_misclass(vcm)
    vcm /= np.sum(vcm, axis=0)

    fig, ax = plt.subplots()
    im = ax.imshow(vcm, cmap=plt.get_cmap('jet'), interpolation='nearest', vmin=0, vmax=1)
    fig.colorbar(im)

    # plot and visualize the confusion matrix.
    plt.xlabel('groud truth y')
    plt.ylabel('predicted y')
    plt.title('voted model on images:%s' % sys.argv[3])
    fname = os.path.dirname(sys.argv[1])+'/voted_confusion_matrix.pdf'
    plt.savefig(os.path.join(fname), bbox_inches='tight')
    plt.show()

    # keep a copy of current labelnames
    save_report(os.path.dirname(sys.argv[1])+'/voted.pkl', vcm, label_names)

