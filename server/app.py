from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from config import main_room
from store import *

socketio = SocketIO()

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

parking_store = Store()

socketio.init_app(app, logger=True, engineio_logger=True)

@socketio.on('enter')
def enter():
    """
    Event triggered by the Raspberry PI when a car enters a lot
    :return:
    """
    #TODO: Implement, and to take care of failures don't allow increments above lot's capacity
    pass

@socketio.on('exit')
def exit():
    """
    Event triggered by the Raspberry PI when a car enters a lot
    :return:
    """
    # TODO: Implement, to take care of failures don't allow decrements below 0
    pass

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
    join_room(main_room)
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

if __name__ == '__main__':
    socketio.run(app)