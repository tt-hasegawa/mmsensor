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
import logging
from PIL import Image
from yolo import YOLO, detect_video
from yolo2 import YOLO2

logging.basicConfig(filename='/tmp/venti-sensor.log', level=logging.DEBUG)

url='https://frozen-reef-90562.herokuapp.com/'
#url='https://192.168.46.128:3000'
proxies = {
    'http': 'http://proxy.matsusaka.co.jp:12080',
    'https': 'http://proxy.matsusaka.co.jp:12080'
}
#proxies = {
#    'http': None,
#    'https': None
#}

logging.info("VentiSensor Start.[{}]".format(url))

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 4
instance = dht11.DHT11(pin=4)
 
# Initialize Camera
camera = picamera.PiCamera()
time.sleep(2)

# analyze picture by AI
yolo = YOLO()
yolo2 = YOLO2()

logging.info("VentiSensor Initialized.")

try:
    while True:
        logging.info("Check Start.")
        temperature=0
        humidity=0
        result = instance.read()
        if result.is_valid():
            temperature=result.temperature
            humidity=result.humidity

        logging.info("Check Temperature:{} Humidity:{}.".format(temperature,humidity))

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
            logging.info("Check Camera People:{}.".format(person))

            uploadData={
		    'temperature':str(temperature),
		    'humidity':str(humidity),
		    'numOfpeople':str(person),
            }
            logging.info(uploadData)
            try:
                with open('out.jpg', 'rb') as f:
                    data = f.read()
                    uploadData['image']=base64.b64encode(data).decode('utf-8')
                    logging.info("POST Start.{}")
                    response = requests.post(url + '/addVentilation/' , json=uploadData, proxies=proxies)
                    logging.info("POST End. {}".format(response.text))
            except Exception as e:
                logging.info(e)
        time.sleep(10)

except KeyboardInterrupt:
    logging.info("Cleanup")
    GPIO.cleanup()

