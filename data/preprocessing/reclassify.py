import pickle
import re
from os import listdir

classes_pkl = open('classes.pkl', 'rb')
mapping_pkl = open('mapping.pkl', 'rb') 
classes = pickle.load(classes_pkl)
mapping = pickle.load(mapping_pkl)

reclassified = {}
for key, value in mapping.iteritems():
    for val in value:
        if not val in reclassified:
            reclassified[val]=[classes[key]]
        else:
            reclassified[val].append(classes[key])

print reclassified
filenames = {}
ls = listdir('../food100/output')
for f in ls:
    m = re.search('img_(.+?)_.*.jpg', f)
    if m is not None:
        if int(m.group(1)) in filenames:
            filenames[int(m.group(1))].append(f)			
        else:
            filenames[int(m.group(1))] = [f]			

for key, value in reclassified.iteritems():
    fnames = []
    for val in value:
        fnames = fnames + filenames[val]
    reclassified[key] = fnames


# Use reclassified as training set for each class:
# ex: reclassified['spaghetti'] = ['img_27_xx', ... , 'img_84_xx']
