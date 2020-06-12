#!/bin/sh

sudo apt-get update

sudo apt-get install libhdf5-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4-dev
sudo apt-get install libqtgui4
sudo apt-get install libqt4-test
sudo apt-get install libcblas-dev
sudo apt-get install libatlas-base-dev

curl https://pjreddie.com/media/files/yolov3.weights -O yolov3.weights
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5

