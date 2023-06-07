"""
patch ROI extracted by yolo localization

"""

import enum 
import sys 
import os 
import glob 
import json 
import time 

import numpy as np 
from PIL import Image
import time 
import cv2 

class patchROI:
    
    def __init__(self,w,h):
        self.frame_size_w = w
        self.frame_size_h = h 

    def black_pad_image(self,pixel,image):
        
        pixel_half = int(pixel/2)
        image_h= image.shape[1]
        image_w=image.shape[0]
        pad_w = int(image_w+pixel)
        pad_h = int(image_h+pixel)

        padded_image = np.zeros((pad_w,pad_h,3))
        padded_image[pixel_half:pixel_half+image_w, pixel_half:pixel_half+image_h]=image


        return padded_image

    def resize_object(self,resize_percent, resize_obj, cropped_image,line):
        w  = cropped_image.shape[0]
        h = cropped_image.shape[1]
        if (round(float(line[5]))-round(float(line[3])))*(round(float(line[4]))-round(float(line[2]))) < 64*64:
            w = int(abs((round(float(line[5]))-round(float(line[3]))))*1.4)
            h = int(abs((round(float(line[4]))-round(float(line[2]))))*1.4)
            #print(w,h)
        elif (round(float(line[5]))-round(float(line[3])))*(round(float(line[4]))-round(float(line[2]))) >256*256 :
            w = int(abs((round(float(line[5]))-round(float(line[3]))))*1)
            h = int(abs((round(float(line[4]))-round(float(line[2]))))*1)
            #print(w,h)
        elif (round(float(line[5]))-round(float(line[3])))*(round(float(line[4]))-round(float(line[2]))) >=64*64 and (round(float(line[5]))-round(float(line[3])))*(round(float(line[4]))-round(float(line[2]))) <=256*256:
            w = int(abs((round(float(line[5]))-round(float(line[3]))))*1)
            h = int(abs((round(float(line[4]))-round(float(line[2]))))*1)
        try :
            cropped_image=cv2.resize(cropped_image, (h,w))
        except Exception as e :
            print(e)
                        

        return cropped_image



    def recursive_packing(self,img, x,y,w,h,patched_image,result,i,sorted_lines,min_w, min_h,f,obj_size, resize_percent, resize_obj):

        if len(sorted_lines)==0:
            return patched_image

        line = sorted_lines[0].split(' ')   
        
        cropped_image = img[round(float(line[3])):round(float(line[5])),round(float(line[2])):(round(float(line[4])))]#top,bottom,left,right
        
        #cropped_image= self.resize_object(resize_percent,resize_obj,cropped_image, line)
        
        height , width , _ = cropped_image.shape
        new_height = int(height *(obj_size/1920))
        new_width = int(width*(obj_size/1920))
        

        try:
            cropped_image = cv2.resize(cropped_image,(new_width,new_height))
        except Exception as e :
            print(e)

                        
        """
        cv2.imshow('patched',cropped_image)

        while True:
            if cv2.waitKey() == ord('q'): # ord는 ASCII 코드로 변환해줌
                break
        """
        #cropped_image = self.black_pad_image(10,cropped_image)
        
        
        priority = 6
        #posible cases with priority 
        if priority >1 and cropped_image.shape[1]==w and cropped_image.shape[0]==h :
            priority =1
        elif priority >2 and cropped_image.shape[1]==w and cropped_image.shape[0]<h :
            priority =2 
        elif priority >3 and cropped_image.shape[1]<w and cropped_image.shape[0]==h :
            priority = 3
        elif priority >4 and cropped_image.shape[1]<w and cropped_image.shape[0]<h :
            priority = 4
        elif priority >5 : 
            priority = 5
        if priority<5:
            omega , d = cropped_image.shape[1], cropped_image.shape[0] #omega = cropped width , d = cropped height
            patched_image[y:y+cropped_image.shape[0],x:x+cropped_image.shape[1]]= cropped_image
            f.write(str(x)+" "+str(y)+" "+str(x+omega)+" "+str(y+d)+" ") #left, top, right, bottom 
            f.write(str(line[2])+" "+str(line[3])+" "+str(line[4])+" "+str(line[5])) #left, top, right, bottom 
            sorted_lines.pop(0)
            #result +=[x,y,x+omega,y+d]
            if priority == 2:
                self.recursive_packing(img,x,y,w,h-d,patched_image,result,i,sorted_lines,min_w, min_h,f,obj_size, resize_percent,resize_obj)

            elif priority ==3:
                self.recursive_packing(img,x+omega,y,w-omega,h,patched_image,result,i,sorted_lines,min_w, min_h,f,obj_size, resize_percent, resize_obj)
            elif priority == 4:
                if w - omega < min_w :
                    self.recursive_packing(img,x,y+d,w,h-d,patched_image,result,i,sorted_lines,min_w, min_h,f,obj_size, resize_percent,resize_obj)

                elif h-d <min_h:
                    self.recursive_packing(img,x+omega,y,w-omega,h,patched_image,result,i,sorted_lines,min_w, min_h,f,obj_size, resize_percent,resize_obj)

                elif omega <min_w :
                    self.recursive_packing(img,x+omega,y,w-omega,d,patched_image,result,i,sorted_lines,min_w, min_h,f,obj_size, resize_percent, resize_obj)
                    self.recursive_packing(img,x,y+d,w,h-d,patched_image,result,1,sorted_lines,min_w, min_h,f,obj_size, resize_percent, resize_obj)

                else:
                    self.recursive_packing(img,x,y+d,omega,h-d,patched_image,result,i,sorted_lines,min_w, min_h,f,obj_size, resize_percent, resize_obj)
                    self.recursive_packing(img,x+omega,y,w-omega,h,patched_image,result,1,sorted_lines,min_w, min_h,f,obj_size, resize_percent, resize_obj)

        return patched_image
           
   
        
    def patch_input_algorithm(self,image_path,roi_info_path,save_patched_image_path,save_patched_info_path,obj_size, resize_percent, resize_obj):
            os.chdir(os.path.dirname(roi_info_path))
            roi_info_list = os.listdir(roi_info_path)
            with open("obj_num_execution_time.txt","w") as txt_file:
                for file in roi_info_list:
                    os.chdir(os.path.dirname(roi_info_path))
                    with open(file) as roi_info:
                        
                        print(roi_info.name)
                        img_name = roi_info.name.strip(".txt")
                        f = open(save_patched_info_path+img_name+'.txt','a')
                        patched_image = np.zeros((self.frame_size_h,self.frame_size_w,3),np.uint8)
                        lines = roi_info.readlines()
                        num_lines = sum(1 for line in lines)
                        #print(lines[0].split(' ')[5])
                        sorted_lines = sorted(lines,key=lambda line: (float(line.split(' ')[4])-float(line.split(' ')[2])),reverse=True) #sort by width 
                        canvas_w =self.frame_size_w
                        canvas_h =self.frame_size_h
                        x=0
                        y=0
                        w=0
                        h=max([(float(line.split(' ')[4])-float(line.split(' ')[2])) for line in sorted_lines])
                        H=0 
                        result = [None]*len(sorted_lines)
                        min_w = min([(float(line.split(' ')[5].split('\n')[0]))-float(line.split(' ')[3]) for line in sorted_lines]) 
                        min_h = min([(float(line.split(' ')[4])-float(line.split(' ')[2])) for line in sorted_lines])
                        
                        
                        for i,read_line in enumerate(sorted_lines):

                            line = read_line.split(' ')   
                            os.chdir(os.path.dirname(image_path))
                            img = cv2.imread(img_name+'.jpg')
                            # <0:class> <1:confidence> <2:left> <3:top> <4:right> <5:bottom>
                            
                            cropped_image = img[round(float(line[3])):round(float(line[5])),round(float(line[2])):(round(float(line[4])))]#top,bottom,left,right

                            """
                            cv2.imshow('patched',cropped_image)
                            while True:
                                if cv2.waitKey() == ord('q'): # ord 는 ASCII 코드로 변환해줌
                                    break                         
                            """
                                # width= shape[1] , height = shape[0] 
                            #print(x,y,cropped_image.shape[1],cropped_image.shape[0])
                            x,y,w,h,H= 0,0,canvas_w,canvas_h ,H+cropped_image.shape[0]
                            start_time = time.time()
                            patched_image=self.recursive_packing(img,x,y,w,h,patched_image,result,i,sorted_lines,min_w, min_h,f,obj_size, resize_percent, resize_obj)
                            x,y = 0,0
                            cv2.imwrite(save_patched_image_path+img_name+'.jpg',patched_image) 
                            #f.write(str(result))
                            end_time = time.time()
                            execution_time = end_time - start_time
                            print(num_lines,execution_time)
                            txt_file.write(str(num_lines))
                            txt_file.write(" ")
                            txt_file.write(str(execution_time))
                            txt_file.write("\n")
                            if i == 0:
                                break 
 

