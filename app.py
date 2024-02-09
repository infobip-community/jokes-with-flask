from flask import Flask, render_template
from infobip_channels.sms.channel import SMSChannel
from jokeapi import Jokes

import os
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('app.html')

async def get_joke_from_api():
    jokes = await Jokes()
    joke = await jokes.get_joke(category=['programming', 'pun'])
    if joke["type"] == "single": # Print the joke
        joke = joke["joke"]
    else:
        joke = f'{joke["setup"]}\n\n{joke["delivery"]}'
    return joke


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
