from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from config import main_room
from store import *

socketio = SocketIO()

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

parking_store = Store()
parking_store.add_lot("hochstetter", 190)

socketio.init_app(app, logger=True, engineio_logger=True)

@socketio.on('enter')
def enter(parking_lot):
    """
    Event triggered by the Raspberry PI when a car enters a lot
    :return:
    """
    store, lot = parking_store.get_store(), parking_lot["name"]
    store[lot].decrease_spots()

@socketio.on('exit')
def exit(parking_lot):
    """
    Event triggered by the Raspberry PI when a car enters a lot
    :return:
    """
    # TODO: Implement, to take care of failures don't allow decrements below 0
    store, lot = parking_store.get_store(), parking_lot["name"]
    store[lot].increase_spots()

@socketio.on('update')
def update():
    """
    Client pings this method for a parking lot update
    :return:
    """
    emit('status', {'store': StoreEncoder().encode(parking_store)}, room=main_room, broadcast = True)

@socketio.on('join')
def join(message):
    """
    Sent by clients when they enter a room.
    """
    join_room(message['room'])
    emit('status', {'store': StoreEncoder().encode(parking_store)}, room=main_room, broadcast = False)

@socketio.on('leave')
def leave(message):
    """
    Sent by clients when they leave a room.
    #TODO: this is probably not necessary
    """
    leave_room(main_room)

@socketio.on('connect')
def connect():
    """
    Both clients and raspberry pis trigger this method automatically when connecting
    :return:
    """
    print(request.sid, " connected")

@socketio.on('disconnect')
def disconnect():
    """
    Both clients and raspberry pis trigger this method automatically when disconnecting
    :return:
    """
    print(request.sid, " disconnected")

def serialize_store():
    """
    Until a better solution as added, serialize the store after every change to make sure we
    can recover if the server goes down
    :return:
    """
    with open("store.json", "w") as file:
        json.dump(parking_store.get_store(), file)

if __name__ == '__main__':
    socketio.run(app)