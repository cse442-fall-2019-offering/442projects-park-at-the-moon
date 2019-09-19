from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet

from config import main_room
from store import *


class App:

    parking_store = None

    def __init__(self):

        self.parking_store = Store()
        self.parking_store.add_lot("hochstetter", 190)
        self.__class__.parking_store = self.parking_store

    def create_app(self):

        app = Flask(__name__)
        app.debug = True
        app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

        from engine import engine
        app.register_blueprint(engine)

        socketio.init_app(app, logger=True, engineio_logger=True)

        return app

socketio = SocketIO()
app_instance = App()

if __name__ == '__main__':

    app = app_instance.create_app()
    app.run()