from PIL import Image
import os

if not os.path.exists("./output/"):
	os.makedirs("./output/")


for item in os.listdir("./"): #explore items (including files)
	if os.path.exists('./'+item+'/'): #if it is a folder
		if os.path.isfile('./'+item+'/bb_info.txt'):
			fo = open('./'+item+'/bb_info.txt', "r+")
			lines = fo.readlines()
			id_message = 1
			for line in lines[1:]:
				split = line.split()
				name_current_image = split.pop(0)+".jpg"
				test_image = './'+item+'/'+name_current_image
				original = Image.open(test_image)
				cropped_example = original.crop((int(split.pop(0)), int(split.pop(0)), int(split.pop(0)), int(split.pop(0))))
				
				cropped_example.save("./output/img_"+item+"_"+str(id_message)+".jpg")
				id_message+=1
