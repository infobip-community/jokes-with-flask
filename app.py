from flask import Flask, render_template, request
from infobip_channels.sms.channel import SMSChannel
from jokeapi import Jokes

import os
import asyncio

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass
    else:
        send_sms_from_app(
            asyncio.run(get_joke_from_api())
        )
    return render_template('app.html')

async def get_joke_from_api():
    jokes = await Jokes()
    joke = await jokes.get_joke(category=['programming', 'pun'], blacklist=['nsfw'])
    if joke["type"] == "single": # Print the joke
        joke = joke["joke"]
    else:
        joke = f'{joke["setup"]}\n\n{joke["delivery"]}'
    return joke


def send_sms_from_app(text):
    channel = SMSChannel.from_env()
    sms_response = channel.send_sms_message({
        'messages': [{
            'from': 'PythonPuns',
            'text': text,
            'destinations': [{
                'to': os.environ['DESTINATION_NUMBER']
            }],
        }]
    })
    print(sms_response)
