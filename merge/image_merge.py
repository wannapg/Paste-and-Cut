from PIL import Image
import os #for time
import time
import cv2 

class Merge:
	def __init__(self,img_dir,save_dir):
		self.img_dir = img_dir
		self.save_dir = save_dir

	void merge(self):

		img_size= [1920,1080]

		start = time.time()

		count = 0
		img_name =''
		new_image = Image.new('RGB',(2*img_size[0], 2*img_size[1]), (250,250,250))

		for image in os.listdir(self.img_dir) : 
		    img = Image.open(os.path.join(self.img_dir,image))
		    if not os.path.exists(self.save_dir):
			os.mkdir(self.save_dir)
		    if count ==0:
			imge_name = ''
			img_name = image 
			new_image = Image.new('RGB',(2*img_size[0], 2*img_size[1]), (250,250,250))
			new_image.paste(img,(0,0))
			count = count+1
		    elif count == 1:
			img_name += '_'+image
			new_image.paste(img,(img_size[0],0))
			count = count +1 
		    elif count == 2:
			img_name += '_'+image
			new_image.paste(img, (0,img_size[1]))
			count = count+1
		    else:
			img_name +='_'+image
			new_image.paste(img, (img_size[0],img_size[1]))
			count = 0
			new_image.save(os.path.join(self.save_dir,img_name+'.jpg'),"JPEG")
		    #new_image.show()
		    #print(count)



		end = time.time()

		print('Execution time : ', end - start,'seconds')
