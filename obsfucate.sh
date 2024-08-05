#!/bin/bash
pyarmor gen config.py
pyarmor gen yolo_app_park.py
pyarmor gen yolo_app_park_trial.py
rm -f config.py
rm -f yolo_app_park.py
rm -f yolo_app_park_trial.py