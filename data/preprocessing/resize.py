from PIL import Image
import os
import sys

if len(sys.argv) < 2:
    print 'Usage : %s <to_size>' % sys.argv[0]
    sys.exit(2)

to_size = int(sys.argv[1])
print 'resizing to %d' % to_size

if not os.path.exists("../food100/output"):
    raise NameError('Images not found')

if not os.path.exists('../food100/output_resized_%d/' % to_size):
    os.makedirs('../food100/output_resized_%d/' % to_size)

for item in os.listdir('../food100/output/'):
    if item.endswith(('.jpg')):
        name_current_image = '../food100/output/'+item
        original_image = Image.open(name_current_image)
        width, height = original_image.size
        smaller_dimension = min(width,height)
        if (max(width,height) / min(width,height) <= 3 ):
            cropped_image = original_image.crop(((width-smaller_dimension)/2 , (height-smaller_dimension)/2,
                                                 (width+smaller_dimension)/2 -1 , (height+smaller_dimension)/2-1))
            resized_image = cropped_image.resize((to_size, to_size), Image.ANTIALIAS)
            output_fname = '../food100/output_resized_%d/%s' % (to_size, item)
            resized_image.save(output_fname)
            print output_fname
