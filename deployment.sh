#!/bin/bash
NV="v0.6"
docker build -t parking_monitoring:$NV .
docker rm parking_monitoring
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="sol" --name parking_monitoring -v /mnt/data/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV
# docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="sol" --name parking_monitoring -v /mnt/data/machine_learning/output:/app/output --gpus all --rm -it parking_monitoring:$NV /bin/bash
