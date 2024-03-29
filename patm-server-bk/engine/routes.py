##############################################################################
#                                 <HEADER>
##############################################################################

from flask import jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from config import main_room
from app import *

from . import engine

parking_store = App.parking_store

@engine.route('/update_spots')
def update_spots():
    """
    Client pings this method for a parking lot update
    :return: Data regarding parking lot empty spots in the JSON format
    """
    return StoreEncoder().encode(app_instance.parking_store)


@engine.route('/car-entered/<lot>')
def car_entered(lot):
    """
    Event triggered by a car entering the parking lot
    :param lot: Name of the parking lot where the event was triggered
    :return:
    """
    app_instance.parking_store.decrease_spots(lot)
    return jsonify()



@engine.route('/car-exited/<lot>')
def car_exited(lot):
    """
    :param lot: Name of the parking lot where a car entered
    :return:
    """
    app_instance.parking_store.increase_spots(lot)
    return jsonify()


##############################################################################
#                               SOCKET EVENTS
# Sockets to be used as backup only
##############################################################################

socketio = SocketIO()


@socketio.on('enter')
def enter(parking_lot):
    """
    Event triggered by the Raspberry PI when a car enters a lot
    :return:
    """
    store, lot = app_instance.parking_store.get_store(), parking_lot["name"]
    store[lot].decrease_spots()


@socketio.on('exit')
def exit(parking_lot):
    """
    Event triggered by the Raspberry PI when a car enters a lot
    :return:
    """
    # TODO: Implement, to take care of failures don't allow decrements below 0
    store, lot = app_instance.parking_store.get_store(), parking_lot["name"]
    store[lot].increase_spots()


@socketio.on('update')
def update():
    """
    Client pings this method for a parking lot update
    :return:
    """
    emit('status', {'store': StoreEncoder().encode(app_instance.parking_store)}, room=main_room, broadcast = True)


@socketio.on('join')
def join(message):
    """
    Sent by clients when they enter a room.
    """
    join_room(message['room'])
    emit('status', {'store': StoreEncoder().encode(app_instance.parking_store)}, room=main_room, broadcast = False)


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

