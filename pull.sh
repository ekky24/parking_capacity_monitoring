#!/bin/bash
git fetch
git pull
git checkout origin/master -- yolo_app_park.py
git checkout origin/master -- yolo_app_park_trial.py
git checkout origin/master -- config.py