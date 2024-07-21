#!/bin/bash

# python "yolo_app_park.py" --source "rtsp" --save-img --device 0 --weights "yolov8m.pt" --classes 2 --parking-capacity 15
python "yolo_app_park.py" --source "CCTV 2.mp4" --save-img --device 0 --weights "yolov8m.pt" --classes 2 --parking-capacity 15