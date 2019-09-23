from flask import Flask
from store import *
from config import SECRET_KEY


class App:

    parking_store = None

    def __init__(self):

        self.parking_store = Store()
        self.parking_store.add_lot("hochstetter", 190)
        self.__class__.parking_store = self.parking_store

    def create_app(self):

        app = Flask(__name__)
        app.debug = True
        app.config['SECRET_KEY'] = SECRET_KEY

        from engine import engine
        app.register_blueprint(engine)

        return app


app_instance = App()

if __name__ == '__main__':

    app = app_instance.create_app()
    app.run()