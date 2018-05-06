import requests
import time
from picamera import PiCamera
import smbus


camera = PiCamera()
address = 0x04
bus = smbus.SMBus(1)

def setup():
	camera.resolution = (640, 480)
	camera.start_preview()


def upload_image():
	camera.capture('pic.jpg')
	fin = open('pic.jpg','rb')
	files = {'file' : fin}

	try:
		r = requests.post("http://104.131.13.68/", files = files)
		print(r.text)

	finally:
		fin.close()

if __name__ == '__main__':
	setup()
	while(True):
		number = bus.read_byte(address)
		print(number)
		if(number == 1):
			upload_image()
			setup()
		time.sleep(1)
