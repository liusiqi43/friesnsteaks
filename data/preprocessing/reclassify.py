import pickle

classes_pkl = open('classes.pkl', 'rb')
mapping_pkl = open('mapping.pkl', 'rb')

classes = pickle.load(classes_pkl)
mapping = pickle.load(mapping_pkl)


