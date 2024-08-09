#!/bin/bash

python "dist/yolo_app_park.py" --source "rtsp" --save-img --device 0 --weights "yolov8l.pt" --classes 2 7 --area $CCTV_AREA