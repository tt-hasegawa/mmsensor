import RPi.GPIO as GPIO
import base64
import cv2
import datetime
import dht11
import numpy as np
import os
import picamera
import requests
import sys
import time
from PIL import Image
from yolo import YOLO, detect_video
from yolo2 import YOLO2

#url='https://protected-caverns-16218.herokuapp.com/'
url='https://192.168.46.128:3000'
#proxies = {
#    'http': 'http://proxy.matsusaka.co.jp:12080',
#    'https': 'http://proxy.matsusaka.co.jp:12080'
#}
proxies = {
    'http': None,
    'https': None
}


# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=14)
 
# Initialize Camera
camera = picamera.PiCamera()
time.sleep(2)

# analyze picture by AI
yolo = YOLO()
yolo2 = YOLO2()

try:
    while True:
        temperature=0
        humidity=0
        result = instance.read()
        if result.is_valid():
            temperature=result.temperature
            humidity=result.humidity

        if temperature > 0 and humidity > 0:
            camera.capture('tmp.jpg')
            image = Image.open('tmp.jpg')
            result = yolo2.detect_image(image)
            r_image=yolo.detect_image(image)
            cv2.imwrite("out.jpg",np.asarray(r_image)[...,::-1])
            
            person=0
            for r in result:
                if r[0].startswith('person'):
                    print(r[0])
                    person+=1

            uploadData={
		    'temperature':str(temperature),
		    'humidity':str(humidity),
		    'numOfpeople':str(person),
            }
            print(uploadData)
            try:
                with open('out.jpg', 'rb') as f:
                    data = f.read()
                    uploadData['image']=base64.b64encode(data).decode('utf-8')
                    print("POST Start. {}".format(response.text))
                    response = requests.post(url + '/addVentilation/' , json=uploadData, proxies=proxies)
                    print("POST End. {}".format(response.text))
            except Exception as e:
                print(e)
        time.sleep(10)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()

