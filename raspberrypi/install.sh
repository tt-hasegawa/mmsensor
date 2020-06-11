#!/bin/sh

sudo apt-get install libavcodec-extra57
sudo apt-get install libavformat57
sudo apt-get install libcblas3 
sudo apt-get install libgstreamer1.0-0
sudo apt-get install libgtk-3
sudo apt-get install libgtk-3-0
sudo apt-get install libharfbuzz0b
sudo apt-get install libhdf5-100
sudo apt-get install libilmbase12
sudo apt-get install libjasper-dev
sudo apt-get install libjasper1
sudo apt-get install libopenexr22
sudo apt-get install libqt4-test
sudo apt-get install libQtGui
sudo apt-get install libswscale4
sudo apt-get install libwebp6

curl https://pjreddie.com/media/files/yolov3.weights -O yolov3.weights
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5

