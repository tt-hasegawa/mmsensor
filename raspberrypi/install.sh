#!/bin/sh

sudo apt-get update

sudo apt-get install libhdf5-dev libjasper-dev libqtgui4-dev libqtgui4 libqt4-test libcblas-dev libatlas-base-dev

curl https://pjreddie.com/media/files/yolov3.weights -O yolov3.weights
python3 convert.py yolov3.cfg yolov3.weights model_data/yolo.h5

