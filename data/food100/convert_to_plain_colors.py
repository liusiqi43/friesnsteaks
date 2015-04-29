from PIL import Image
import os
import sys
import numpy as np
import random



for item in os.listdir('../food100/output_resized_64/'):
    if item.endswith(('.jpg')):
        name_current_image = '../food100/output_resized_64/'+item
        original_image = Image.open(name_current_image)

        if item.startswith(('img_98')):
		color=str(random.randrange(1,50))
		new_image = Image.new("RGB", (64, 64), 'rgb('+color+','+color+','+color+')')
		

        if item.startswith(('img_61')):
		color=str(random.randrange(245,255))
		new_image = Image.new("RGB", (64, 64), 'rgb('+color+','+color+','+color+')')
        output_fname = '../food100/output_resized_64/%s' % (item)
        new_image.save(output_fname)
        print output_fname
