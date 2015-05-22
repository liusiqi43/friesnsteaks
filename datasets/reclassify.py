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
        'rice' : ['rice'],
        'eels on rice' : ['grilled fish'],
        'pilaf' : ['mixed rice'],
        'beef curry' : ['curry rice'],
        'sushi' : ['sushi'],
        'chicken rice' : ['mixed rice'],
        'fried rice' : ['mixed rice'],
        'tempura bowl' : ['tempura'],
        'bibimbap' : ['bibimbap'],
        'toast' : ['bread'],
        'croissant' : ['croissant'],
        'roll bread' : ['croissant'],
        'raisin bread' : ['bread'],
        'chip butty' : ['chip butty'],
        'hamburger' : ['hamburger'],
        'pizza' : ['pizza'],
        'sandwiches' : ['sandwich'],
        'udon noodle' : ['noodle soup'],
        'tempura udon': ['noodle soup'],
        'soba noodle': ['noodle '],
        'ramen noodle': ['noodle soup'],
        'beef noodle': ['noodle soup'],
        'fried noodle': ['noodle'],
        'spaghetti': ['noodle'],
        'gratin' : ['gratin'],
        'sauteed vegetables' : ['sauteed vegetables'],
        'croquette' : ['croquette'],
        'grilled eggplant': ['eggplant'],
        'sauteed spinach' : ['sauteed spinach'],
        'vegetable tempura' : ['tempura'],
        'miso soup' : ['soup'],
        'potage': ['potage'],
        'sausage' : ['sausage'],
        'omelet': ['omelet'],
        'jiaozi': ['jiaozi'],
        'stew': ['stew'],
        'teriyaki grilled fish': ['grilled fish'],
        'fried fish': ['fried fish'],
        'grilled salmon': ['grilled fish'],
        'salmon meuniere': ['grilled fish'],
        'sashimi': ['sushi'],
        'grilled pacific saury': ['grilled pacific saury'],
        'sukiyaki': ['sukiyaki'],
        'sweet and sour pork': ['sweet and sour pork'],
        'lightly roasted fish': ['grilled fish'],
        'steamed egg hotchpotch': ['steamed eggs'],
        'tempura': ['tempura'],
        'fried chicken': ['fried chicken'],
        'sirloin cutlet': ['sirloin cutlet'],
        'nanbanzuke': ['nanbanzuke'],
        'boiled fish': ['boiled fish'],
        'seasoned beef with potatoes': ['seasoned beef with potatoes'],
        'hambarg steak': ['steak'],
        'steak': ['steak'],
        'dried fish': ['dried fish'],
        'ginger pork saute': ['ginger pork saute'],
        'spicy chili-flavored tofu': ['spicy chili-flavored tofu'],
        'yakitori': ['brochette'],
        'cabbage roll': ['cabbage roll'],
        'omelet': ['omelet'],
        'egg sunny-side up': ['egg sunny-side up'],
        'natto': ['natto'],
        'cold tofu': ['tofu'],
        'egg roll': ['egg roll'],
        'chilled noodle': ['noodle'],
        'stir-fried beef and peppers': ['stir-fried beef and peppers'],
        'simmered pork': ['simmered pork'],
        'boiled chicken and vegetables': ['boiled chicken and vegetables'],
        'sashimi bowl': ['sushi'],
        'sushi bowl': ['sushi'],
        'fish-shaped pancake with bean jam': ['fish-shaped pancake'],
        'shrimp with chill source': ['shrimp with sauce'],
        'roast chicken': ['roast chicken'],
        'steamed meat dumpling': ['steamed meat dumpling'],
        'omelet with fried rice': ['omelet'],
        'cutlet curry': ['curry rice'],
        'spaghetti meat sauce': ['noodle'],
        'fried shrimp': ['fried shrimp'],
        'potato salad': ['potato salad'],
        'green salad': ['green salad'],
        'macaroni salad': ['macaroni salad'],
        'Japanese tofu and vegetable chowder': ['soup'],
        'pork miso soup': ['soup'],
        'chinese soup': ['soup'],
        'beef bowl': ['beef bowl'],
        'kinpira-style sauteed burdock': ['kinpira'],
        'rice ball': ['rice ball'],
        'pizza toast': ['pizza toast'],
        'dipping noodles': ['noodle'],
        'hot dog':['hot dog'],
        'french fries': ['french fries'],
        'mixed rice': ['mixed rice']
    }
    return mapping

def get_classes():
    classes = {
        'rice':  1,
        'eels on rice':  2,
        'pilaf':  3,
        'chicken-n-egg on rice':  4,
        'pork cutlet on rice':  5,
        'beef curry':  6,
        'sushi':  7,
        'chicken rice':  8,
        'fried rice':  9,
        'tempura bowl':  10,
        'bibimbap':  11,
        'toast':  12,
        'croissant':  13,
        'roll bread':  14,
        'raisin bread':  15,
        'chip butty':  16,
        'hamburger':  17,
        'pizza':  18,
        'sandwiches':  19,
        'udon noodle':  20,
        'tempura udon':  21,
        'soba noodle':  22,
        'ramen noodle':  23,
        'beef noodle':  24,
        'tensin noodle':  25,
        'fried noodle':  26,
        'spaghetti':  27,
        'Japanese-style pancake':  28,
        'takoyaki':  29,
        'gratin':  30,
        'sauteed vegetables':  31,
        'croquette':  32,
        'grilled eggplant':  33,
        'sauteed spinach':  34,
        'vegetable tempura':  35,
        'miso soup':  36,
        'potage':  37,
        'sausage':  38,
        'oden':  39,
        'omelet':  40,
        'ganmodoki':  41,
        'jiaozi':  42,
        'stew':  43,
        'teriyaki grilled fish':  44,
        'fried fish':  45,
        'grilled salmon':  46,
        'salmon meuniere':  47,
        'sashimi':  48,
        'grilled pacific saury':  49,
        'sukiyaki':  50,
        'sweet and sour pork':  51,
        'lightly roasted fish':  52,
        'steamed egg hotchpotch':  53,
        'tempura':  54,
        'fried chicken':  55,
        'sirloin cutlet':  56,
        'nanbanzuke':  57,
        'boiled fish':  58,
        'seasoned beef with potatoes':  59,
        'hambarg steak':  60,
        'steak':  61,
        'dried fish':  62,
        'ginger pork saute':  63,
        'spicy chili-flavored tofu':  64,
        'yakitori':  65,
        'cabbage roll':  66,
        'omelet':  67,
        'egg sunny-side up':  68,
        'natto':  69,
        'cold tofu':  70,
        'egg roll':  71,
        'chilled noodle':  72,
        'stir-fried beef and peppers':  73,
        'simmered pork':  74,
        'boiled chicken and vegetables':  75,
        'sashimi bowl':  76,
        'sushi bowl':  77,
        'fish-shaped pancake with bean jam':  78,
        'shrimp with chill source':  79,
        'roast chicken':  80,
        'steamed meat dumpling':  81,
        'omelet with fried rice':  82,
        'cutlet curry':  83,
        'spaghetti meat sauce':  84,
        'fried shrimp':  85,
        'potato salad':  86,
        'green salad':  87,
        'macaroni salad':  88,
        'Japanese tofu and vegetable chowder':  89,
        'pork miso soup':  90,
        'chinese soup':  91,
        'beef bowl':  92,
        'kinpira-style sauteed burdock':  93,
        'rice ball':  94,
        'pizza toast':  95,
        'dipping noodles':  96,
        'hot dog':  97,
        'french fries':  98,
        'mixed rice':  99,
        'goya chanpuru':  100
    }
    return classes

def reclassify(which_set, img_size=128):
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
    ls = os.listdir(os.path.join(__location__, \
                                 '../data/food100/output_%d/%s' % (img_size, which_set)))
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
            try:
                fnames = fnames + filenames[val]
            except KeyError:
                print which_set
                print filenames
                print reclassified[key]
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
