import socketio
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from config import hostname, main_room
import requests


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
scheduler = BackgroundScheduler()
sio = socketio.Client()

@sio.on('connect')
def connect():
    join()
    print('connection established')

@sio.on('status')
def status(data):
    print(data['store'])

@sio.on('disconnect')
def disconnect():
    print('disconnected from server')

def update():
    r = requests.get(hostname + '/update_spots')
    import json
    print(json.loads(r.content))

def join():
    sio.emit('join', {'room': main_room})

if __name__ == '__main__':
    #sio.connect(hostname)
    job = scheduler.add_job(update, 'interval', seconds = 5)
    scheduler.start()
    while True:
        pass