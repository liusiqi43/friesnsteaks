from PIL import Image
import os

if not os.path.exists("../food100/output"):
    raise NameError('Images not found')	

if not os.path.exists('../food100/output_resized/'):
    os.makedirs('../food100/output_resized/')

for item in os.listdir('../food100/output/'): 
    if item.endswith(('.jpg')):
        name_current_image = '../food100/output/'+item
        original_image = Image.open(name_current_image)
        width, height = original_image.size
        smaller_dimension = min(width,height)
        if (max(width,height) / min(width,height) <= 3 ):
            cropped_image = original_image.crop(((width-smaller_dimension)/2 , (height-smaller_dimension)/2, 
                                                 (width+smaller_dimension)/2 -1 , (height+smaller_dimension)/2-1))
            resized_image = cropped_image.resize((128,128), Image.ANTIALIAS)
            output_fname = '../food100/output_resized/'+item
            resized_image.save(output_fname)
            print output_fname
