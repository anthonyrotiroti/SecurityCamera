from flask import Flask
from twilio.rest import Client

account_sid = "ACd92719d546df4f489edcb425f5cf1cd6"
auth_token = "cc1ea46b9de3d7c453e8116f81792011"
client = Client(account_sid, auth_token)
app = Flask(__name__)

@app.route('/')
def send_message():
	
	message = client.messages \
	                .create(
	                     body="Hey buddy",
	                     from_="+15162267545",
	                     to="+19145821416"
	                 )

	return ("Message should've been sent hopefully")
	
if __name__ == '__main__':
	app.run()
