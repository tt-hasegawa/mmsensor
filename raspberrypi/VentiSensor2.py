import logging
import mh_z19
import time
import requests


logging.basicConfig(filename='/tmp/venti-sensor2.log', level=logging.DEBUG)

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

logging.info("VentiSensor Initialized.")


while True:
	try:
		uploadData = mh_z19.read()
		print(uploadData)
		logging.info(uploadData)
		response = requests.post(url + '/addVentilation2/' , json=uploadData, proxies=proxies)
	except Exception as e:
		logging.info(e)
	time.sleep(10)

