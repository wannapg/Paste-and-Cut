from unittest import result
from PIL import Image
import os #for time
import time
import cv2 
import numpy as np 
from PIL import ImageChops

def calcdiff(im1,im2):
    dif = ImageChops.difference(im1,img2)
    return np.mean(np.array(dif))

dir =  '/home/rtcl/다운로드/test/MOT16-14/img1'
save_dir = '/home/rtcl/workspace/yolov5'
img1 = Image.new('RGB',(1920,1080),(250,250,250))
img2 = Image.new('RGB', (1920,2080),(250,250,250))
count =0 
num =0
similarity_num =0 
for image in os.listdir(dir) : 
    print(num)
    if count == 0:
        img1 = Image.open(os.path.join(dir,image))
        count = count +1 
    else :
        img2 = Image.open(os.path.join(dir,image))
        count = 0 
        similarity_num= calcdiff(img1, img2)
    
    with open(os.path.join(save_dir,'similarity.txt'),"a") as f:
            f.write(f'{similarity_num}\n')
            f.close()
    num = num+1