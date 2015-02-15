#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle

output = open('mapping.pkl', 'wb')

# Critère: étant donné un nom de classe, est-ce qu'on réfléchit à ces images
# 'cooked noodle': 'noodle' without soup
# 'noodle soup': 'noodle' with soup
# 'raw fish' visually quite different from other fish. 
mapping = {
    'rice' : ['rice'], 
    'eels on rice' : ['grilled', 'fish', 'grilled fish'],
    'pilaf' : ['mixed rice'],
    'beef curry' : ['curry rice'],
    'sushi' : ['sushi', 'raw fish'],
    'chicken rice' : ['mixed rice'],
    'fried rice' : ['mixed rice'],
    'tempura bowl' : ['tempura', 'fried', 'fried shrimp'],
    'bibimbap' : ['mixed vegetables'],
    'toast' : ['toast', 'bread'],
    'croissant' : ['croissant'],
    'roll bread' : ['croissant'],
    'raisin bread' : ['bread'],
    'chip butty' : ['sandwich'],
    'hamburger' : ['hamburger'],
    'pizza' : ['pizza'],
    'sandwiches' : ['sandwich'],
    'udon noodle' : ['noodle', 'noodle soup'],
    'tempura udon': ['tempura', 'noodle', 'noodle soup'],
    'soba noodle': ['noodle', 'cooked noodle'],
    'ramen noodle': ['noodle', 'noodle soup'],
    'beef noodle': ['noodle', 'noodle soup'],
    'fried noodle': ['noodle', 'cooked noodle'],
    'spaghetti': ['noodle', 'spaghetti'],
    'gratin' : ['gratin', 'melted cheese'],
    'sauteed vegetables' : ['sauteed vegetables'],
    'croquette' : ['fried', 'croquette'],
    'grilled eggplant': ['eggplant'],
    'sauteed spinach' : ['sauteed vegetables', 'spinach'],
    'vegetable tempura' : ['tempura', 'fried'],
    'miso soup' : ['soup'],
    'potage': ['soup'],
    'sausage' : ['sausage'],
    'omelet': ['omelet'],
    'jiaozi': ['jiaozi'],
    'stew': ['stew'],
    'teriyaki grilled fish': ['grilled', 'fish', 'grilled fish'],
    'fried fish': ['fried', 'fried fish'],
    'grilled salmon': ['grilled', 'fish', 'grilled fish'],
    'salmon meuniere ': ['grilled', 'fish', 'grilled fish'],
    'sashimi': ['raw fish'],
    'grilled pacific saury ': ['grilled', 'fish', 'grilled fish', 'fish with skin'],
    'sukiyaki': ['stew', 'mixed vegetables'],
    'sweet and sour pork': ['sweet and sour', 'pork', 'vegetables with meat'],
    'lightly roasted fish': ['fish', 'raw fish'],
    'steamed egg hotchpotch': ['steamed eggs'],
    'tempura': ['tempura', 'fried'],
    'fried chicken': ['fried','fried chicken'],
    'sirloin cutlet ': ['fried','croquette'],
    'nanbanzuke': ['fish and vegetables','fish with skin'],
    'boiled fish': ['fish', 'boiled fish', 'fish with skin'],
    'seasoned beef with potatoes': ['potatoes', 'vegetables with meat'],
    'hambarg steak': ['steak', 'meat'],
    'steak': ['steak', 'meat'],
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
    'chilled noodle': ['mixed vegetables', 'chilled noodle', 'noodle'],
    'stir-fried beef and peppers': ['vegetables with meat'],
    'simmered pork': ['meat'],
    'boiled chicken and vegetables': ['vegetables with meat'],
    'sashimi bowl': ['mixed rice', 'raw fish'],
    'sushi bowl': ['mixed rice'],
    'fish-shaped pancake with bean jam': ['fish-shaped pancake'],
    'shrimp with chill source': ['shrimp'],
    'roast chicken': ['grilled', 'grilled chicken'],
    'steamed meat dumpling': ['steamed meat dumpling', 'dumpling'],
    'omelet with fried rice': ['omelet'],
    'cutlet curry': ['curry rice'],
    'spaghetti meat sauce': ['noodle', 'spaghetti'],
    'fried shrimp': ['fried', 'fried shrimp'],
    'potato salad': ['potato salad', 'salad'],
    'green salad': ['green salad', 'salad'],
    'macaroni salad': ['macaroni salad', 'salad'],
    'Japanese tofu and vegetable chowder': ['soup', 'tofu and vegetable'],
    'pork miso soup': ['pork miso soup', 'soup'],
    'chinese soup': ['soup'],
    'beef bowl': ['beef', 'shredded beef', 'shredded'],
    'kinpira-style sauteed burdock': ['vegetables'],
    'rice ball': ['rice ball'],
    'pizza toast': ['pizza toast', 'toast'],
    'dipping noodles': ['noodle'],
    'hot dog':['hot dog'],
    'french fries': ['french fries'],
    'mixed rice': ['mixed rice']
}

pickle.dump(mapping, output)
output.close()