import os
from flask import Flask, request, redirect, url_for, send_from_directory
from twilio.rest import Client
import config


client = Client(config.sid,config.key)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/var/www/SecurityCamera/SecurityCamera/static'

@app.route('/', methods=['GET','POST'])
def recieve_file():
        if request.method == 'POST':
                file = request.files['file']
                if file:
                        filename = file.filename
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],'pic.jpg'))
                       	message = client.messages \
	                		.create(
		                     body="*** INTRUDER DETECTED ***",
		                     from_= config.number_from,
		                     to= config.number_to,
		                     media_url="http://104.131.13.68/static/pic.jpg"
	                 )
                        return 'good'
        return 'bad'
if __name__ == '__main__':
        app.run()

