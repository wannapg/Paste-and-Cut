- 환경 설정은 활용하고자 하는 dnn 모델에 따라 진행

- Dataset
  MOT(Multi object Tracking) Dataset 
  https://motchallenge.net/data/MOT16/
  
- Detection Model: YOLOv5 
  https://github.com/ultralytics/yolov5/tree/v7.0
  
- mAP 측정 도구
  https://github.com/Cartucho/mAP
  <class_name> <left> <top> <right> <bottom> 형식으로 txt 파일을 구성해야함. 

- 구성
  Merge : 이미지 병합 코드
  Patching : RoI를 하나의 patch frame으로 구성하는 코드 
  Mapping : 기존의 이미지 혹은 mAP 측정 도구 형식으로 mapping하는 코드
  Size Decision : Merge Patch 사이즈 결정 코드 
  Util : gpu utilization 측정(gpu_utilization.py), frame 간 similarity 비교(frame_similarity.py), object size 측정(object_size_to_txt.py),object occupancy 측정(object_occupancy.py), txt 파일을 map 측정 format으로 변경(txt_to_maptool_format.py)  등 유틸리티 코드
  Experiment Results: 실험 결과 그래프 모음
  
  main.py 를 작성하는 경우 다음 순서로 진행 : 
  Merge -> (localization 모델) -> RoI Patching -> (classification 모델) -> Mapping -> mAP 측정
  
