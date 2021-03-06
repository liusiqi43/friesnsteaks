from PIL import Image
from glob import glob
from random import choice, random, uniform, randint

import os
import sys
import threading

inputs = glob('data/food100/[1-9]*/bb_info.txt')

def which_set():
    rnd = random()
    if rnd < 0.75:
        return 'train'
    elif rnd < 0.9:
        return 'test'
    else:
        return 'valid'

def invalid(box):
    min_size = 30
    return box[0]+min_size >= box[2] or box[1]+min_size >= box[3]

def rotate(input_image, start, end):
    return input_image.rotate(randint(start, end))

def flip(input_image):
    methods = [Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM]
    if random() > 1./(len(methods)+1):
        return input_image.transpose(choice(methods))
    else:
        return input_image

def agitate(size, box):
    new_box = [int(point + uniform(-10, 10) + .5) for point in box]
    return cramp(size, new_box)

def cramp(size, box):
    box[0] = max(0, min(size[1]-1, box[0]))
    box[2] = max(0, min(size[1]-1, box[2]))
    box[1] = max(0, min(size[0]-1, box[1]))
    box[3] = max(0, min(size[0]-1, box[3]))
    return box

def resize(img, to_size):
    width, height = img.size
    smaller_dimension = min(width,height)
    if (max(width,height) / min(width,height) <= 3):
        cropped_image = img.crop(((width-smaller_dimension)/2, \
                                  (height-smaller_dimension)/2, \
                                  (width+smaller_dimension)/2-1, \
                                  (height+smaller_dimension)/2-1))
        return cropped_image.resize((to_size, to_size), Image.ANTIALIAS)

def get_box_centered(img, coordinates):
    left = coordinates[0]
    high = coordinates[1]
    right = coordinates[2]
    down = coordinates[3]
    width, height = img.size
    extended = min(left - 0, high - 0, width - right, height - down)
    coordinates[0]=max(0,left - extended)
    coordinates[1]=max(0,high - extended)
    coordinates[2]=min(width, right + extended)
    coordinates[3]=min(height, down + extended)
    return 



class Preprocessor(threading.Thread):
    def __init__(self, to_size, begin, end, inputs):
        threading.Thread.__init__(self)
        self.begin = begin
        self.end = end
        self.inputs = inputs
        self.to_size = to_size


    def run(self):
        for item in inputs[self.begin:self.end]:
            class_id = item.split('/')[2]
            count = len(glob('data/food100/%s/*.jpg' % class_id))

            with open(item, 'r+') as fo:
                lines = fo.readlines()
                id_img = 1
                for line in lines[1:]:
                    which = which_set()
                    split = map(int, line.split())
                    input_id, coordinates = split[0], split[1:]
                    input_image = 'data/food100/%s/%d.jpg' % (class_id, input_id)
                    original = Image.open(input_image)
                    fname = 'data/food100/output_%d/%s/img_%s_%d.jpg' \
                        % (self.to_size, which, class_id, id_img)
                    resized = resize(original.crop(coordinates), self.to_size)
                    if resized is None:
                        continue
                    resized.save(fname)
                    id_img += 1
                    if (which == 'train'):
                        for i in xrange(max(1, min(2, int(500/count)))):
                            
                            box = agitate(original.size, coordinates)
                            if invalid(box):
                                continue
                            
                            #Adrien
                            cordinates_centered = get_box_centered(original,coordinates) 
                            ready_to_be_rotated = original.crop(coordinates_centered)
                            output_flip = flip(ready_to_be_rotated)
                            resized_and_flip = resize(output_flip, self.to_size) 
                            


                            cropped = original.crop(box)
                            #output = rotate(flip(cropped), -30, 30)
                            output = flip(cropped)
                            resized = resize(output, self.to_size)
                            if resized is None:
                                continue
                            fname = 'data/food100/output_%d/%s/img_%s_%d.jpg' \
                                % (self.to_size, which, class_id, id_img)
                            resized.save(fname)
                            id_img += 1
                print 'Working on %s with %d images, generated %d images' \
                    % (item, count, id_img)

def main():
    if len(sys.argv) < 2:
        print 'Usage : %s <to_size>' % sys.argv[0]
        sys.exit(2)

    to_size = int(sys.argv[1])
    print 'preprocessing to size %d' % to_size

    if not os.path.exists('data/food100/output_%d/' % to_size):
        os.makedirs('data/food100/output_%d/train' % to_size)
        os.makedirs('data/food100/output_%d/test' % to_size)
        os.makedirs('data/food100/output_%d/valid' % to_size)
    else:
        print 'output folder already exists'
        sys.exit(-1)

    nbatches = int(sys.argv[2])
    starts = [i*len(inputs)/nbatches for i in xrange(nbatches)]
    ends = [i*len(inputs)/nbatches for i in xrange(1, nbatches+1)]

    threads = []
    for i in xrange(len(starts)):
        print 'thread #%d: working on classes [%d, %d[...' \
            % (i, starts[i], ends[i])
        thread = Preprocessor(to_size, starts[i], ends[i], inputs)
        thread.start()
        threads.append(thread)

    for x in threads:
        x.join()

    print 'done...'
    print 'ntrain: %d' % len(glob('data/food100/output_%d/train/*.jpg' % to_size))
    print 'ntest: %d' % len(glob('data/food100/output_%d/test/*.jpg' % to_size))
    print 'nvalid: %d' % len(glob('data/food100/output_%d/valid/*.jpg' % to_size))

if __name__ == '__main__':
    main()
