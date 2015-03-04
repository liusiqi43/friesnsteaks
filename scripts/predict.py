import PIL, numpy as np, sys, theano
from PIL import Image
from pylearn2.utils import serial
from theano import tensor as T

#must be placed in pylearn2/pylearn2/scripts/tutorials/softmax_regression/
model_path = 'softmax_regression_best.pkl'
model = serial.load( model_path )

X = model.get_input_space().make_theano_batch()
Y = model.fprop(X)

Y = T.argmax( Y, axis = 1)

f = theano.function([X], Y)

img = Image.open(sys.argv[1]).convert("L")
np_img = np.array(img)
np_img_flatten = np.reshape(np_img,(1,784))
		
print( f(np_img_flatten ))
	

while True:
	x = raw_input('Nom d\'image ? (q pour quitter)')	
	if x == 'q':
		break
	else:
		img = Image.open(x).convert("L")
		np_img = np.array(img)
		np_img_flatten = np.reshape(np_img,(1,784))
		
		print( f(np_img_flatten ))
	
