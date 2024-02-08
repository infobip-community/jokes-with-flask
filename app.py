from flask import Flask
from infobip_channels.sms.channel import SMSChannel

import os

app = Flask(__name__)

@app.route('/')
def index():
    
    return "<p>hello world</p>"

def send_sms_from_app(text):
    channel = SMSChannel.from_env()
    sms_response = channel.send_sms_message({
        'messages': [{
            'text': 'This text came from your Flask app!',
            'destinations': [{
                'to': os.environ['DESTINATION_NUMBER']
            }],
        }]
    })
    print(sms_response)
