#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle

output = open('mapping.pkl','wb')

# Critère: étant donné un nom de classe, est-ce qu'on réfléchit à ces images
#'cooked noodle':'noodle' without soup
#'noodle soup':'noodle' with soup
#'raw fish' visually quite different from other fish.
mapping = {
   'steak': ['steak'],
   'french fries': ['french fries'],
}

pickle.dump(mapping, output)
output.close()
