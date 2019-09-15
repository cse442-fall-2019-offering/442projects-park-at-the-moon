import socketio
from flask import Flask
from config import hostname
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
scheduler = BackgroundScheduler()
sio = socketio.Client()

@sio.on('connect')
def connect():
    print('connection established')

@sio.on('status')
def status(data):
    print('parking lot status: ', data)

@sio.on('disconnect')
def disconnect():
    print('disconnected from server')

def enter():
    sio.emit('enter')
    print("car entered")

def exit():
    sio.emit('exit')
    print("car exited")

def join():
    sio.emit('join', {})

if __name__ == '__main__':
    sio.connect(hostname)
    join()
    scheduler.add_job(enter, 'interval', seconds = 10)
    scheduler.add_job(exit, 'interval', seconds=15)
    scheduler.start()