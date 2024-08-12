#!/bin/bash
chmod 755 config.py
chmod 755 yolo_app_park.py
chmod 755 yolo_app_park_trial_2.py
pyarmor gen config.py
pyarmor gen yolo_app_park.py
pyarmor gen yolo_app_park_trial_2.py
rm -f config.py
rm -f yolo_app_park.py
rm -f yolo_app_park_trial_2.py