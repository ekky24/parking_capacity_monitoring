#!/bin/bash
pyarmor gen config.py
pyarmor gen yolo_app_park.py
pyarmor gen yolo_app_park_web.py
pyarmor gen yolo_app_park_web_2.py
rm -f config.py
rm -f yolo_app_park.py
rm -f yolo_app_park_web.py
rm -f yolo_app_park_web_2.py