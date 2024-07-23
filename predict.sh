#!/bin/bash

python "yolo_app_park.py" --source "rtsp" --save-img --device 0 --weights "yolov8m.pt" --classes 2 --area $CCTV_AREA