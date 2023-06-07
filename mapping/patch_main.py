
import enum
import sys 
import os 
import glob
import json 
import time

from split_label import SplitLabel
from patch_roi import patchROI
from patched_mapping import MapPatched
from patched_mapping import IntersectGtDrFiles

import shutil


def run_yolo():
    imgsz = [1920,1856,1792,1792,1664,1600,1536,1472,1408,1344,1280,1216,1152,1088,1024,960,896,832,768,704,640,576,512,448,384,320,256]
    imgsz_h = [1088,1056,1024,992,960,928,964,832,800,768,736,704,672,640,600,608,576,544,512,480,448,416,384,352,320,228,256]
    merged_imgsz =  256

    for i,value in enumerate(imgsz):

        imgsz = value
        dir = '/home/rtcl/workspace/yolov5/patch/mer'+str(merged_imgsz)+'/'+str(value)+'/patched_image/'
        command = f"python execution_time.py --save-txt --save-conf --source {dir} --imgsz {imgsz} "
        os.system(command)

def run_yolo_obj():
    percent = {2}
    resize_obj ={'test'}
    for resize_obj_size in resize_obj: 
        for i,value in enumerate(percent):
            imgsz = 1
            dir = '/home/rtcl/workspace/yolov5/patch/mer640/'+str(value)+'/patched_image/'
            command = f"python execution_time.py --save-txt --save-conf --source {dir} --imgsz {imgsz} "
            os.system(command)


def main_maptool_format_input_obj():
    patcher = MapPatched()

    for i in range(1):
        img_w = 1920
        img_h=1088
        save_dir =''
        if i==0:
            dir = '/home/rtcl/workspace/yolov5/runs/detect/exp11/labels/'
            save_dir = '/home/rtcl/workspace/yolov5/runs/detect/exp11/mapped_labels/'
        else:   
            dir = '/home/rtcl/workspace/yolov5/runs/detect/exp'+ str(i+1)+'/labels/'
            save_dir = '/home/rtcl/workspace/yolov5/runs/detect/exp'+ str(i+1)+'/mapped_labels/'
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        os.mkdir(save_dir)
        patcher.txt_to_maptool_format_input(dir, save_dir, 1920, 1080)

def main_mapping_obj():
    patcher = MapPatched()

    data = ['09']
    percent = {2}
    resize_obj ={'test'}
    for resize_obj_size in resize_obj: 
        for i,value in enumerate(percent):
            dir =''
            if i==0:
                dir = '/home/rtcl/workspace/yolov5/runs/detect/exp/mapped_labels/'
            else:   
                dir = '/home/rtcl/workspace/yolov5/runs/detect/exp'+ str(i+1)+'/mapped_labels/'
            patched_info_dir = '/home/rtcl/workspace/yolov5/patch/object_size/'+resize_obj_size+'/'+str(value)+'/patched_info/'
            save_dir = '/home/rtcl/workspace/mAP/input/detection-results/object_size/'+resize_obj_size+'/'+str(value)+'/'
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
            os.mkdir(save_dir)
            print(dir)

            patcher.map_input(dir, patched_info_dir,save_dir,obj_size=1920)

def main_intersect_obj():
    
    intersect = IntersectGtDrFiles()

    percent = {2}
    resize_obj ={'test'}
    for resize_obj_size in resize_obj: 
        for i,value in enumerate(percent):
            GT_PATH = '/home/rtcl/workspace/mAP/input/ground-truth/MOT16-09/'
            DR_PATH =  '/home/rtcl/workspace/mAP/input/detection-results/object_size/'+resize_obj_size+'/'+str(value)+'/mapped/'
            intersect.intersect_gt_and_dr(GT_PATH,DR_PATH)
            
def main_maptool_format_input():
    patcher = MapPatched()
    imgsz =[1920]
    imgsz_h =[1088]

    data =['09']
    for i,value in enumerate(imgsz):

        img_w = value
        img_h= imgsz_h[i]
        save_dir =''
        if i==0:
            dir = '/home/rtcl/workspace/yolov5/runs/detect/exp12/labels/'
            save_dir = '/home/rtcl/workspace/yolov5/runs/detect/exp12/mapped_labels/'
        else:   
            dir = '/home/rtcl/workspace/yolov5/runs/detect/exp'+ str(i+1)+'/labels/'
            save_dir = '/home/rtcl/workspace/yolov5/runs/detect/exp'+ str(i+1)+'/mapped_labels/'
            shutil.rmtree(save_dir)
        os.mkdir(save_dir)
        patcher.txt_to_maptool_format_input(dir, save_dir, 1920, 1080)

def main_mapping():
    patcher = MapPatched()
    imgsz = [1920,1856,1792,1792,1664,1600,1536,1472,1408,1344,1280,1216,1152,1088,1024,960,896,832,768,704,640,576,512,448,384,320,256]
    imgsz_h = [1088,1056,1024,992,960,928,964,832,800,768,736,704,672,640,600,608,576,544,512,480,448,416,384,352,320,228,256]
    data = ['09']
    merged_size =  256

    for i,value in enumerate(imgsz):
        dir =''
        if i==0:
            dir = '/home/rtcl/workspace/yolov5/runs/detect/exp/mapped_labels/'
        else:   
            dir = '/home/rtcl/workspace/yolov5/runs/detect/exp'+ str(i+1)+'/mapped_labels/'
        patched_info_dir = '/home/rtcl/workspace/yolov5/patch/mer'+str(merged_size)+'/'+str(value)+'/patched_info/'
        save_dir = '/home/rtcl/workspace/mAP/input/detection-results/final/mer'+str(merged_size)+'/'
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        save_dir = '/home/rtcl/workspace/mAP/input/detection-results/final/mer'+str(merged_size)+'/'+str(value)+'/'
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        os.mkdir(save_dir)
        print(dir)
        patcher.map_input(dir, patched_info_dir,save_dir,obj_size=value)


            
def main_intersect():
    
    intersect = IntersectGtDrFiles()
    imgsz_h = [1088,1056,1024,992,960,928,964,832,800,768,736,704,672,640,600,608,576,544,512,480,448,416,384,352,320,228,256]
    merged_size =   256


    imgsz =[1920]
    for i,value in enumerate(imgsz):
        GT_PATH = '/home/rtcl/workspace/mAP/input/ground-truth/MOT16-09/'
        DR_PATH = '/home/rtcl/workspace/mAP/input/detection-results/loc/'
        intersect.intersect_gt_and_dr(GT_PATH,DR_PATH)

def main_split_label():
    dataset =  ['09']
    split = SplitLabel()
    imgsz = [1920,1856,1792,1792,1664,1600,1536,1472,1408,1344,1216,1152,1088,896,832,768,704,640]
    merge_sizes = [1024, 960,896,832,768,704,640,576,512,448,384,320,256]


    for i,value in enumerate(merge_sizes):
        imgsz = value
        save_dir =''
        dir = '/home/rtcl/workspace/yolov5/runs/detect/mer'+str(value)+'/labels/'
        save_dir = '/home/rtcl/workspace/yolov5/runs/detect/mer'+str(value)+'/splited_labels/'
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        os.mkdir(save_dir)
        split.split_input_dir(dir,save_dir)

def main_vanilla():
    main_maptool_format_input()
    main_intersect()

def main_merged():
    main_split_label()
    main_maptool_format_input()
    main_intersect()

def main_patched():
    main_maptool_format_input()
    main_mapping()
    main_intersect()

if __name__ =="__main__":
    
    main_vanilla()
    main_merged()
    
    """
    run_yolo_obj()
    main_maptool_format_input_obj()
    main_mapping_obj()
    main_intersect_obj()
    """
    #main_maptool_format_input_obj()

    #run_yolo()
    #main_patched()
    #main_intersect()



