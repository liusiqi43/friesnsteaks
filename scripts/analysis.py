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

np.set_printoptions(threshold=np.nan)

def get_model_function(model_path):
    model = serial.load(model_path)
    print model
    X = model.get_input_space().make_theano_batch()
    Y = model.fprop(X)
    return theano.function([X], Y)

def get_np_img(img_path, show=False):
    img = Image.open(img_path)
    if show:
        img.show()
    return np.asarray(img, dtype=theano.config.floatX)/127. - 1.

def get_np_imgs(img_paths, imageShape, id_to_class, class_to_superclass, class_to_label):
    data = np.zeros((len(img_paths), ) + imageShape, dtype=theano.config.floatX)
    ytrue = np.zeros(len(img_paths))
    for i, path in enumerate(img_paths):
        fname = os.path.basename(path)
        data[i] = get_np_img(path)
        ytrue[i] = class_to_label[class_to_superclass[id_to_class[int(fname.split('_')[1])]][0]]

    return data, ytrue

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print 'Usage: analysis.py <path/to/model.pkl> <path/to/images> <number of batches>'
        sys.exit(-1)

    f = get_model_function(sys.argv[1])
    # 'data/food100/output_resized_64/img_61_*.jpg'
    datapath = sys.argv[2]
    batch = int(sys.argv[3])


    class_to_id = get_classes()
    id_to_class = {v: k for k, v in class_to_id.items()}
    class_to_superclass = get_mapping()

    label_names_pkl_path = os.path.join(string_utils.preprocess('${PYLEARN2_DATA_PATH}'), 'food100', 'label_names.pkl')
    label_names_pkl = open(label_names_pkl_path, 'rb')
    label_names = pickle.load(label_names_pkl)
    class_to_label = {l : i for i, l in enumerate(label_names)}
    label_names_pkl.close()

    print 'Loading from: %s' % datapath
    result = np.zeros((len(label_names), len(label_names)), dtype=float)
    print 'result matrix size: %s' % str(result.shape)
    test_set = [img for img in glob(datapath) if class_to_superclass.has_key(id_to_class[int(os.path.basename(img).split('_')[1])])]

    imageShape = get_np_img(test_set[0]).shape
    batch_size = len(test_set)/batch
    for i in xrange(batch):
        print 'processing batch #%d' % i
        images, ytrue = get_np_imgs(test_set[i*batch_size:(i+1)*batch_size], imageShape, id_to_class, class_to_superclass, class_to_label)
        res = f(images)
        ypred = np.argmax(res, axis=1)
        cm = confusion_matrix(ytrue, ypred, range(len(label_names))).astype(float)
        result += cm

    # column major normalization.
    #         ytrue
    #       ----------
    #       |        |
    # ypred |        |
    #       |        |
    #       ----------

    result /= np.sum(result, axis=0)

    fig, ax = plt.subplots()
    im = ax.imshow(result, cmap=plt.get_cmap('jet'), interpolation='nearest', vmin=0, vmax=1)
    fig.colorbar(im)

    # keep a copy of current labelnames
    label_names_path = sys.argv[1].split('.')[-2]+'_labelname.csv'
    with open(label_names_path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['predicted_class_id', 'label'])
        for i, label in enumerate(label_names):
            writer.writerow([i, label])

    worst_classes_path = sys.argv[1].split('.')[-2]+'_worstclasses.csv'
    with open(worst_classes_path, 'wb') as csvfile:
        k = 5
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['true class'] + k * ['predicted'])
        # find out the worst_performing classes.
        # worst_classes contains the worst performing 10 classes, in decreasing order of misclass rate.
        worst_classes = np.argsort(result.diagonal())
        confusion_with = np.argsort(result, axis=0)
        for cls in worst_classes:
            # top k classes that are confused with class cls
            row = [cls] + confusion_with[-1:-2-k:-1, cls].tolist()
            row = ['%s:%.2f' % (label_names[c], result[c, cls]) for c in row]
            writer.writerow(row)

    # plot and visualize the confusion matrix.
    plt.xlabel('groud truth y')
    plt.ylabel('predicted y')
    plt.title('model:%s; images:%s' % (sys.argv[1].split('.')[-2], sys.argv[2]))
    fname = sys.argv[1].split('.')[-2]+'_confusion_matrix.pdf'
    plt.savefig(os.path.join(fname), bbox_inches='tight')
    plt.show()
