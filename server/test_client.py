import socketio
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from config import hostname

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

def update():
    sio.emit('update')
    print("requesting update")

def join():
    sio.emit('join', {})

if __name__ == '__main__':
    sio.connect(hostname)
    join()
    job = scheduler.add_job(update, 'interval', seconds = 5)
    scheduler.start()