from PIL import Image
import os

if not os.path.exists("../food100/output/"):
	os.makedirs("../food100/output/")


for item in os.listdir("../food100/"): 
	if os.path.isdir('../food100/'+item):
		fo = open('../food100/'+item+'/bb_info.txt', "r+")
		lines = fo.readlines()
		id_message = 1
		for line in lines[1:]:
			split = line.split()
			name_current_image = split.pop(0)+".jpg"
			test_image = '../food100/'+item+'/'+name_current_image
			original = Image.open(test_image)
			cropped_example = original.crop((int(split.pop(0)), int(split.pop(0)), int(split.pop(0)), int(split.pop(0))))
			
			cropped_example.save("../food100/output/img_"+item+"_"+str(id_message)+".jpg")
			id_message+=1
