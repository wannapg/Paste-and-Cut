import sys 
import os 
import glob
import json 

det_txt_path ='/home/rtcl/workspace/yolov5/runs/detect/exp42/labels/'
save_det_txts_path ='/home/rtcl/workspace/mAP/input/detection-results/MOT16-09/' 

labels = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic-light',
        'fire-hydrant', 'stop-sign', 'parking-meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports-ball', 'kite', 'baseball-bat', 'baseball-glove', 'skateboard', 'surfboard',
        'tennis-racket', 'bottle', 'wine-glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot-dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted-plant', 'bed', 'dining-table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell-phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy-bear',
        'hair-drier', 'toothbrush']

#chdir
os.chdir(os.path.dirname(det_txt_path))
file_list = os.listdir(det_txt_path)
file_list.sort()
count = 1


#patched
image_width = 1920
image_height = 1080

for filename in file_list:
    os.chdir(os.path.dirname(det_txt_path))
    with open(filename) as det_file:
        while True:
            line = det_file.readline()
            if line=="":
                break
            line = line.split(' ')
            #<class> <1:x> <2:y> <3:w> <4:h> <5:confidence>
            os.chdir(os.path.dirname(save_det_txts_path))
            
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
            f.write(str(image_width*(float(line[1])-float(line[3])/2)))#left x-w/2
            f.write(" ")
            f.write(str(image_height*(float(line[2])-float(line[4])/2)))#top y-h/2
            f.write(" ")
            f.write(str(image_width*(float(line[1])+float(line[3])/2))) #right x+w/2
            f.write(" ")
            f.write(str(image_height*(float(line[2])+float(line[4])/2))) #bottom y+h/2
            f.write("\n")
            f.close()
            
    count+=1 
