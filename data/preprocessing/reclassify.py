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
        'eels on rice' : ['grilled','fish','grilled fish'],
        'pilaf' : ['mixed rice'],
        'beef curry' : ['curry rice'],
        'sushi' : ['sushi','raw fish'],
        'chicken rice' : ['mixed rice'],
        'fried rice' : ['mixed rice'],
        'tempura bowl' : ['tempura','fried','fried shrimp'],
        'bibimbap' : ['mixed vegetables'],
        'toast' : ['toast','bread'],
        'croissant' : ['croissant'],
        'roll bread' : ['croissant'],
        'raisin bread' : ['bread'],
        'chip butty' : ['sandwich'],
        'hamburger' : ['hamburger'],
        'pizza' : ['pizza'],
        'sandwiches' : ['sandwich'],
        'udon noodle' : ['noodle','noodle soup'],
        'tempura udon': ['tempura','noodle','noodle soup'],
        'soba noodle': ['noodle','cooked noodle'],
        'ramen noodle': ['noodle','noodle soup'],
        'beef noodle': ['noodle','noodle soup'],
        'fried noodle': ['noodle','cooked noodle'],
        'spaghetti': ['noodle','spaghetti'],
        'gratin' : ['gratin','melted cheese'],
        'sauteed vegetables' : ['sauteed vegetables'],
        'croquette' : ['fried','croquette'],
        'grilled eggplant': ['eggplant'],
        'sauteed spinach' : ['sauteed vegetables','spinach'],
        'vegetable tempura' : ['tempura','fried'],
        'miso soup' : ['soup'],
        'potage': ['soup'],
        'sausage' : ['sausage'],
        'omelet': ['omelet'],
        'jiaozi': ['jiaozi'],
        'stew': ['stew'],
        'teriyaki grilled fish': ['grilled','fish','grilled fish'],
        'fried fish': ['fried','fried fish'],
        'grilled salmon': ['grilled','fish','grilled fish'],
        'salmon meuniere': ['grilled','fish','grilled fish'],
        'sashimi': ['raw fish'],
        'grilled pacific saury': ['grilled','fish','grilled fish','fish with skin'],
        'sukiyaki': ['stew','mixed vegetables'],
        'sweet and sour pork': ['sweet and sour','pork','vegetables with meat'],
        'lightly roasted fish': ['fish','raw fish'],
        'steamed egg hotchpotch': ['steamed eggs'],
        'tempura': ['tempura','fried'],
        'fried chicken': ['fried','fried chicken'],
        'sirloin cutlet': ['fried','croquette'],
        'nanbanzuke': ['fish and vegetables','fish with skin'],
        'boiled fish': ['fish','boiled fish','fish with skin'],
        'seasoned beef with potatoes': ['potatoes','vegetables with meat'],
        'hambarg steak': ['steak','meat'],
        'steak': ['steak','meat'],
        'dried fish': ['fish','dried fish'],
        'ginger pork saute': ['vegetables and meat'],
        'spicy chili-flavored tofu': ['mixed tofu'],
        'yakitori': ['brochette'],
        'cabbage roll': ['cabbage roll'],
        'omelet': ['omelet'],
        'egg sunny-side up': ['sunny-side up'],
        'natto': ['natto'],
        'cold tofu': ['tofu'],
        'egg roll': ['egg roll'],
        'chilled noodle': ['mixed vegetables','chilled noodle','noodle'],
        'stir-fried beef and peppers': ['vegetables with meat'],
        'simmered pork': ['meat'],
        'boiled chicken and vegetables': ['vegetables with meat'],
        'sashimi bowl': ['mixed rice','raw fish'],
        'sushi bowl': ['mixed rice'],
        'fish-shaped pancake with bean jam': ['fish-shaped pancake'],
        'shrimp with chill source': ['shrimp'],
        'roast chicken': ['grilled','grilled chicken'],
        'steamed meat dumpling': ['steamed meat dumpling','dumpling'],
        'omelet with fried rice': ['omelet'],
        'cutlet curry': ['curry rice'],
        'spaghetti meat sauce': ['noodle','spaghetti'],
        'fried shrimp': ['fried','fried shrimp'],
        'potato salad': ['potato salad','salad'],
        'green salad': ['green salad','salad'],
        'macaroni salad': ['macaroni salad','salad'],
        'Japanese tofu and vegetable chowder': ['soup','tofu and vegetable'],
        'pork miso soup': ['pork miso soup','soup'],
        'chinese soup': ['soup'],
        'beef bowl': ['beef','shredded beef','shredded'],
        'kinpira-style sauteed burdock': ['vegetables'],
        'rice ball': ['rice ball'],
        'pizza toast': ['pizza toast','toast'],
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
                                 '../food100/output_%d/%s' % (img_size, which_set)))
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
