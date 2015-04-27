# -*- coding: utf-8 -*-

import pickle
import re
import os, sys
from pprint import pprint

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_mapping():
    # Critere: étant donné un nom de classe, est-ce qu'on réfléchit à ces images
    #'cooked noodle':'noodle' without soup
    #'noodle soup':'noodle' with soup
    #'raw fish' visually quite different from other fish.
    mapping = {
       'steak': ['steak'],
       'french fries': ['french fries'],
    }
    return mapping

def get_classes():
    classes = {
            'steak':  61,
            'french fries':  98,
    }
    return classes

def reclassify(img_size=128):
    classes = get_classes()
    mapping = get_mapping()

    reclassified = {}
    for key, value in mapping.iteritems():
        for val in value:
            if not val in reclassified:
                reclassified[val]=[classes[key]]
            else:
                reclassified[val].append(classes[key])

    filenames = {}
    ls = os.listdir(os.path.join(__location__, '../food100/output_resized_%d' % img_size))
    for f in ls:
        m = re.search('img_(.+?)_.*.jpg', f)
        if m is not None:
            if int(m.group(1)) in filenames:
                filenames[int(m.group(1))].append(f)
            else:
                filenames[int(m.group(1))] = [f]

    example_count = {}
    for key, value in reclassified.iteritems():
        fnames = []
        for val in value:
            fnames = fnames + filenames[val]
        example_count[key] = len(fnames)
        reclassified[key] = fnames

    image_to_labels = {}
    for label, images in reclassified.iteritems():
        for img in images:
            if image_to_labels.has_key(img):
                image_to_labels[img].append(label)
            else:
                image_to_labels[img] = [label]

    # Use reclassified as training set for each class:
    # ex: reclassified['spaghetti'] = ['img_27_xx', ... , 'img_84_xx']
    return image_to_labels, reclassified, example_count
