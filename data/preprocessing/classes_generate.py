#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle

output = open('classes.pkl', 'wb')

classes = {
        'steak':  61,
        'french fries':  98,
}

pickle.dump(classes, output)
output.close()
