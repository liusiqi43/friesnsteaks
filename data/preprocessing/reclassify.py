import pickle
import re
import os, sys
from pprint import pprint

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def reclassify():
    classes_pkl = open(os.path.join(__location__, 'classes.pkl'), 'rb')
    mapping_pkl = open(os.path.join(__location__, 'mapping.pkl'), 'rb') 
    classes = pickle.load(classes_pkl)
    mapping = pickle.load(mapping_pkl)

    reclassified = {}
    for key, value in mapping.iteritems():
        for val in value:
            if not val in reclassified:
                reclassified[val]=[classes[key]]
            else:
                reclassified[val].append(classes[key])

    filenames = {}
    ls = os.listdir(os.path.join(__location__, '../food100/output_resized'))
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

    # pprint(example_count)
    print '{} classes, with an average of {} examples per class.'.format(len(reclassified), sum(example_count.values())/len(reclassified))
    print 'A total of {} examples.'.format(sum(example_count.values()))

    # Use reclassified as training set for each class:
    # ex: reclassified['spaghetti'] = ['img_27_xx', ... , 'img_84_xx']
    return reclassified, example_count
