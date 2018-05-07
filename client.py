import requests
import time
from picamera import PiCamera
import RPi.GPIO as GPIO
import math

camera = PiCamera()
GPIO.setmode(GPIO.BCM)

TRIG = 19
ECHO = 13
LED = 26

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

is_connected = True
distance = 0


def setup():
	camera.resolution = (640, 480)
	camera.rotation = 180
	camera.start_preview()
	time.sleep(2.5)

	

def upload_image():
	global is_connected

	print("Taking picture...")
	camera.capture('pic.jpg')
	fin = open('pic.jpg','rb')
	files = {'file' : fin}

	try:
		print("Sending picture...")
		r = requests.post("http://104.131.13.68/", files = files)
		print(r.text)
	
	except:
		is_connected = False
		print('connection failed')

	finally:
		fin.close()

def get_distance():
	GPIO.output(TRIG, True)
	time.sleep(0.000001)
	GPIO.output(TRIG, False)
	
	start_time = time.time()
	stop_time = time.time()
	
	while GPIO.input(ECHO) == 0:
		start_time = time.time()
	
	while GPIO.input(ECHO) == 1:
		stop_time = time.time()

	time_elapsed = stop_time - start_time
	return  (time_elapsed * 34300)/2
		
	
if __name__ == '__main__':
	setup()
	print('Calibrating distance')
	distances = []
	for i in range(8):
		distances.append(get_distance())
		time.sleep(0.5)

	distance = sum(distances)/len(distances)
	threshold = distance / 10
	print('standard distance set to: %d' % distance)
	print(distance)
	print('alert distance set to: %d' % threshold)
	print(threshold)
	
	while(is_connected):
		print(get_distance())
		GPIO.output(LED, True)
		if(get_distance() < threshold):
			GPIO.output(LED, False)
			upload_image()
			setup()
		time.sleep(0.2)
	#No connection
	
	led_on = True
	print('CONNECTION LOST')
	while(True):
		GPIO.output(LED, led_on)
		time.sleep(0.5)
		led_on = not led_on

		
