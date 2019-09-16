import socketio
from flask import Flask
from config import hostname, pi_room
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
scheduler = BackgroundScheduler()
sio = socketio.Client()

def enter():
    sio.emit('enter', {"name": "hochstetter"})
    print("car entered")

def exit():
    sio.emit('exit', {"name": "hochstetter"})
    print("car exited")

def join():
    sio.emit('join', {'room': pi_room})

@sio.on('connect')
def connect():
    join()
    print('connection established')

@sio.on('status')
def status(data):
    print('parking lot status: ', data)

@sio.on('disconnect')
def disconnect():
    print('disconnected from server')

if __name__ == '__main__':
    sio.connect(hostname)
    scheduler.add_job(enter, 'interval', seconds = 2)
    scheduler.add_job(exit, 'interval', seconds=10)
    scheduler.start()