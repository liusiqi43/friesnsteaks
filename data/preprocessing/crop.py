from PIL import Image
import os

if not os.path.exists("../food100/output/"):
	os.makedirs("../food100/output/")


for class_id in os.listdir("../food100/"): 
	bb_info_fname = '../food100/'+class_id+'/bb_info.txt'
	if os.path.isfile(bb_info_fname):
		fo = open(bb_info_fname, "r+")
		lines = fo.readlines()
		id_img = 1
		for line in lines[1:]:
			split = line.split()
			name_current_image = split.pop(0)+".jpg"
			test_image = '../food100/'+class_id+'/'+name_current_image
			original = Image.open(test_image)
			cropped_example = original.crop((int(split.pop(0)), int(split.pop(0)), int(split.pop(0)), int(split.pop(0))))
			output_fname = "../food100/output/img_"+class_id+"_"+str(id_img)+".jpg"
			cropped_example.save(output_fname)
			id_img += 1
			print output_fname
