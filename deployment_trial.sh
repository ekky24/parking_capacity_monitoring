#!/bin/bash
NV="trial"
docker build -f Dockerfile_trial -t parking_monitoring:$NV .

# Solaria
# docker stop parking_monitoring_sol
# docker rm parking_monitoring_sol
docker run -d -p 0.0.0.0:5050:5050 --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="sol" --name parking_monitoring_sol_trial --network app-network -v /mnt/data/machine_learning/output:/app/output --gpus all --restart unless-stopped parking_monitoring:$NV