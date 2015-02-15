from PIL import Image
import os

if not os.path.exists("./output/"):
	os.makedirs("./output/")


for root, dirs, files in os.walk("./"): #current directory
	for name in files:
		if name.endswith(("bb_info.txt")):
			fo = open(os.path.join(root,name), "r+")
			line = fo.readlines();
			a = True;
			#numerotation des images
			i = 1;
			for s in line:
				l = s.split();
				#On jump la premiere ligne
				if a:
					a = False;
				else:
					name1= l.pop(0)+".jpg";
					test_image = os.path.join(root,name1);
					original = Image.open(test_image);
					cropped_example = original.crop((int(l.pop(0)), int(l.pop(0)), int(l.pop(0)), int(l.pop(0))))
					if "/" in root:
						param, value = root.split("/",1)
					cropped_example.save("./output/"+value+"_"+str(i)+".jpg")
					i+=1