#!/bin/sh
curl https://pjreddie.com/media/files/yolov3.weights -O yolov3.weights
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5

