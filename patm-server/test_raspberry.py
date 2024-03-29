import socketio
import requests
from flask import Flask
from config import hostname, pi_room, SECRET_KEY
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = SECRET_KEY
scheduler = BackgroundScheduler()
sio = socketio.Client()


def car_entered(lot):
    requests.get(hostname + '/car-entered/' + lot)


def car_exited(lot):
    requests.get(hostname + '/car-exited/' + lot)


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
    scheduler.start()
    scheduler.add_job(car_entered, 'interval', ['hochstetter'], seconds = 2)
    scheduler.add_job(car_exited, 'interval', ['hochstetter'], seconds=10)
    while True:
        pass
