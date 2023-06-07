import enum
import sys 
import os 
import glob
import json 
import time

from split_label import SplitLabel
from patch_roi import patchROI

labels = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic-light',
        'fire-hydrant', 'stop-sign', 'parking-meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports-ball', 'kite', 'baseball-bat', 'baseball-glove', 'skateboard', 'surfboard',
        'tennis-racket', 'bottle', 'wine-glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot-dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted-plant', 'bed', 'dining-table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell-phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy-bear',
        'hair-drier', 'toothbrush']

#original img로 변환
class MapPatched:
    def __init__(self):
        self.maptool_det_txt_path ='/home/rtcl/workspace/mAP/input/detection-results/MOT16-04/split_labels 640/'
        self.maptool_save_det_txts_path='/home/rtcl/workspace/mAP/input/detection-results/MOT16-04/to_map_format 640/' 

        self.det_txt_path ='/home/rtcl/workspace/mAP/input/detection-results/patched_results/MOT16-02/split_lab
        self.save_det_txts_path ='/home/rtcl/workspace/mAP/input/detection-results/patched_results/MOT16-02/to_map_format 2048/' 
        self.patched_info_path ='/home/rtcl/workspace/mmdetection/crop/MOT16-09_K25/patched_datatxt/'

        #original image size
        self.image_width = 1920
        self.image_height = 1080

    def __init__(self, p1,p2,p3,p4,p5,w,h):
        self.maptool_det_txt_path =p1
        self.maptool_save_det_txts_path=p2

        self.det_txt_path =p3
        self.save_det_txts_path =p4
        self.patched_info_path =p5

        #original image size
        self.image_width = w
        self.image_height = h

    
    def map(self):
        #chdir
        execution_f = open('/home/rtcl/workspace/mAP/input/detection-results/k25_mapping_execution_time.txt','a') #execution time
        os.chdir(os.path.dirname(self.det_txt_path))
        file_list = os.listdir(self.det_txt_path)
        
        count = 0

        det_file = ''
        patch_file = ''
        
        for filename in file_list:
            start_time = time.time()
            img_name = str(filename)
            print(img_name)
            os.chdir(os.path.dirname(self.det_txt_path))
            det_file = open(filename,'r')
            os.chdir(os.path.dirname(self.patched_info_path))
            patch_file = open(filename ,'r')
            
            #read patch info lines
            patch_lines = patch_file.readlines()
            patch_line = []
            for i, patch in enumerate(patch_lines):
                patch_line.append(patch.split(' '))

                #detfile <0:class> <1:confidence> <2:left> <3:top> <4:right> <5:bottom>
                #
                #patch file  <0:patch_left> <1:patch_top> <2: patch_right> <3: patch_bottom> 
                #            <4: original_l> <5: original_t> <6: original_r> <7: original_b>  
                #
                #final file  <0:class> <1:confidence> <2:left> <3:top> <4:right> <5:bottom>
                
                
            #obj matching
            while True:
                #read a detection 
                det_line = det_file.readline()
                if det_line== "" :
                    break 
                det_line = det_line.split(' ')


                #print(det_line)
                #get detection center coordinates
                center_x =float(det_line[2])+(float(det_line[4]) -float(det_line[2]))/2 #right-left 
                center_y= float(det_line[3])+(float(det_line[5])-float(det_line[3]))/2

                final_left =0 
                final_top =0
                #print('center',center_x,center_y)
                
                #match objects with confidence higher than 0.5
                #if det_line >0.5 :
                #    continue
                

                #find object section in patched image
                for i, patch in enumerate(patch_line):
                    #check mid x,y fits in the section
                    #check center x 
                    if int(patch[0])<= center_x and center_x<=int(patch[2]):
                        #check center y
                        if int(patch[1])<=center_y and center_y<=int(patch[3]):
                            if patch[4]=='\n':
                                break 
                            else:
                                final_left =float(det_line[2])-int(patch[0])+int(patch[4])
                                final_top = float(det_line[3])-int(patch[1])+int(patch[5])
                                break 

                    
                os.chdir(os.path.dirname(self.save_det_txts_path))
                f = open(img_name,'a')
                f.write((str(det_line[0]))) #class
                f.write(" ")
                f.write(str(float(det_line[1])))#confidence
                f.write(" ")
                f.write(str(final_left))#left
                f.write(" ")
                f.write(str(final_top))#top
                f.write(" ")
                f.write(str(final_left+(float(det_line[4])-float(det_line[2]))))#right
                f.write(" ")
                f.write(str(final_top+(float(det_line[5])-float(det_line[3]))))#bottom
                f.write("\n")
                f.close()
                
            execution_f.write(str(time.time()-start_time))
            execution_f.write("\n")
        execution_f.close()

    def map_input(self,detected_dir,patched_info_dir,save_mapped_dir,obj_size):

        os.chdir(os.path.dirname(detected_dir))
        file_list = os.listdir(detected_dir)
        
        count = 0
        
        for filename in file_list:
            start_time = time.time()
            img_name = str(filename)
            print(img_name)
            os.chdir(os.path.dirname(detected_dir))
            det_file = open(filename,'r')
            os.chdir(os.path.dirname(patched_info_dir))
            patch_file = open(filename ,'r')
            
            #read patch info lines
            patch_lines = patch_file.readlines()
            patch_line = []
            for i, patch in enumerate(patch_lines):
                patch_line.append(patch.split(' '))


                #detfile <0:class> <1:confidence> <2:left> <3:top> <4:right> <5:bottom>
                #
                #patch file  <0:patch_left> <1:patch_top> <2: patch_right> <3: patch_bottom> 
                #            <4: original_l> <5: original_t> <6: original_r> <7: original_b>  
                #
                #final file  <0:class> <1:confidence> <2:left> <3:top> <4:right> <5:bottom>
                
                
            #obj matching
            while True:
                #read a detection 
                det_line = det_file.readline()
                if det_line== "" :
                    break 
                det_line = det_line.split(' ')

                #get detection center coordinates
                center_x =float(det_line[2])+(float(det_line[4]) -float(det_line[2]))/2 #right-left 
                center_y= float(det_line[3])+(float(det_line[5])-float(det_line[3]))/2

                final_left =0 
                final_top =0

                #find object section in patched image
                for i, patch in enumerate(patch_line):
                    #check mid x,y fits in the section
                    #check center x 
                    if float(patch[0])<= center_x and center_x<=float(patch[2]):
                        #check center y
                        if float(patch[1])<=center_y and center_y<=float(patch[3]):
                            #if patch[4]=='\n':
                            #    break 
                            #else:
                            final_left =float(det_line[2])-float(patch[0])+float(patch[4])
                            final_top = float(det_line[3])-float(patch[1])+float(patch[5])
                            break 

                    
                os.chdir(os.path.dirname(save_mapped_dir))
                os.makedirs('./mapped',exist_ok=True)
                os.chdir('./mapped')
                f = open(img_name,'a')
                f.write((str(det_line[0]))) #class
                f.write(" ")
                f.write(str(float(det_line[1])))#confidence
                f.write(" ")
                f.write(str(final_left))#left
                f.write(" ")
                f.write(str(final_top))#top
                f.write(" ")
                f.write(str(final_left+(float(det_line[4])-float(det_line[2]))*(1920/obj_size)))#right
                f.write(" ")
                f.write(str(final_top+(float(det_line[5])-float(det_line[3]))*(1920/obj_size)))#bottom
                f.write("\n")
                f.close()
                

    def txt_to_maptool_format(self):
        #txt_to_map_format
        #chdir
        os.chdir(os.path.dirname(self.maptool_det_txt_path))
        file_list = os.listdir(self.maptool_det_txt_path)
        file_list.sort()
        count = 1


        for filename in file_list:
            os.chdir(os.path.dirname(self.maptool_det_txt_path))
            with open(filename) as det_file:
                while True:
                    line = det_file.readline()
                    if line=="":
                        break
                    line = line.split(' ')
                    #<class> <1:x> <2:y> <3:w> <4:h> <5:confidence>
                    os.chdir(os.path.dirname(self.maptool_save_det_txts_path))
                    
                    i = len(str(count))
                    file_name = str(count)
                    while i<6:
                        i+=1
                        file_name= '0' +file_name
                    
                    f = open(file_name+'.txt','a')

                    f.write(str(labels[int(float(line[0]))])) #class name
                    f.write(" ")
                    line[5]  = line[5].strip('\n')
                    f.write((line[5])) #confidence
                    f.write(" ")
                    f.write(str(self.image_width*abs(float(line[1])-float(line[3])/2)))#left x-w/2
                    f.write(" ")
                    f.write(str(self.image_height*abs(float(line[2])-float(line[4])/2)))#top y-h/2
                    f.write(" ")
                    f.write(str(self.image_width*abs(float(line[1])+float(line[3])/2))) #right x+w/2
                    f.write(" ")
                    f.write(str(self.image_height*abs(float(line[2])+float(line[4])/2))) #bottom y+h/2
                    f.write("\n")
                    f.close()
                    
            count+=1 

    def txt_to_maptool_format_input(self,dir,save_dir,imgsz_w,imgsz_h):
        #txt_to_map_format
        #chdir
        os.chdir(os.path.dirname(dir))
        file_list = os.listdir(dir)
        file_list.sort()
        count = 1


        for filename in file_list:
            os.chdir(os.path.dirname(dir))
            with open(filename) as det_file:
                while True:
                    line = det_file.readline()
                    if line=="":
                        break
                    line = line.split(' ')
                    #<class> <1:x> <2:y> <3:w> <4:h> <5:confidence>
                    os.chdir(os.path.dirname(save_dir))
                    i = len(str(count))
                    file_name = str(count)
                    while i<6:
                        i+=1
                        file_name= '0' +file_name
                    
                    f = open(file_name+'.txt','a')

                    
                    f.write(str(labels[int(float(line[0]))])) #class name
                    f.write(" ")
                    line[5]  = line[5].strip('\n')
                    f.write((line[5])) #confidence
                    f.write(" ")
                    if (float(line[1])-float(line[3])/2) >= 0:
                        f.write(str((imgsz_w*float(line[1])-imgsz_w*(float(line[3])/2))))#left x-w/2
                    else :
                        f.write("0")
                    f.write(" ")
                    if (float(line[2])-float(line[4])/2)>=0:
                        f.write(str(imgsz_h*(float(line[2])-float(line[4])/2)))#top y-h/2
                    else :
                        f.write("0")
                    f.write(" ")
                    f.write(str(imgsz_w*(float(line[1])+float(line[3])/2))) #right x+w/2
                    f.write(" ")
                    f.write(str(imgsz_h*(float(line[2])+float(line[4])/2))) #bottom y+h/2
                    f.write("\n")
                    f.close()
                    
            count+=1


class IntersectGtDrFiles:
    def __init__(self):
        self.path = ''

    def intersect_gt_and_dr(self,GT_PATH,DR_PATH):
        backup_folder = 'backup_no_matches_found' # must end without slash

        os.chdir(GT_PATH)
        gt_files = glob.glob('*.txt')
        if len(gt_files) == 0:
            print("Error: no .txt files found in", GT_PATH)
            sys.exit()
        os.chdir(DR_PATH)
        dr_files = glob.glob('*.txt')
        if len(dr_files) == 0:
            print("Error: no .txt files found in", DR_PATH)
            sys.exit()

        gt_files = set(gt_files)
        dr_files = set(dr_files)
        print('total ground-truth files:', len(gt_files))
        print('total detection-results files:', len(dr_files))
        print()

        gt_backup = gt_files - dr_files
        dr_backup = dr_files - gt_files

        def backup(src_folder, backup_files, backup_folder):
            # non-intersection files (txt format) will be moved to a backup folder
            if not backup_files:
                print('No backup required for', src_folder)
                return
            os.chdir(src_folder)
            ## create the backup dir if it doesn't exist already
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            for file in backup_files:
                os.rename(file, backup_folder + '/' + file)
            
        backup(GT_PATH, gt_backup, backup_folder)
        backup(DR_PATH, dr_backup, backup_folder)
        if gt_backup:
            print('total ground-truth backup files:', len(gt_backup))
        if dr_backup:
            print('total detection-results backup files:', len(dr_backup))

        intersection = gt_files & dr_files
        print('total intersected files:', len(intersection))
        print("Intersection completed!")

        
