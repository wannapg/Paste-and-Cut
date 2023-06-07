from PIL import Image
import os #for time
import time
import cv2 




img1_dir =  '/home/rtcl/workspace/samples/CAM_BACK'
img_size= [1600,480]

start = time.time()

count = 0
num = 0
new_image = Image.new('RGB',(2*img_size[0], 2*img_size[1]), (250,250,250))

for image in os.listdir(img1_dir) : 
    img = Image.open(os.path.join(img1_dir,image))
    if count ==0:
        new_image = Image.new('RGB',(2*img_size[0], 2*img_size[1]), (250,250,250))
        new_image.paste(img,(0,0))
        count = count+1
    else:
        new_image.paste(img,(img_size[0],0))
        count = 0
        new_image.save(os.path.join("/home/rtcl/workspace/samples/MERGED_CAM_BACK_2/",str(num)+'.jpg'),"JPEG")
        num = num+1 
    #new_image.show()
    print(count)



end = time.time()

print('Execution time : ', end - start,'seconds')
