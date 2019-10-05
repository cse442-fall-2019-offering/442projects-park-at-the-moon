import sys,os
import json
from flask import Flask
from store import *
from config import SECRET_KEY

app = None

class App:

    parking_store = None

    def __init__(self):

        self.parking_store = Store()
        data = None
        with open("lot_data.json") as file:
            data = json.load(file)
        for lot in data['lots']:
            name = lot["name"]
            self.parking_store.add_lot(name, lot["capacity"])
            self.parking_store.set_available_times(name, lot["available_times"])
            self.parking_store.set_boundary_lat(name, lot["boundary_lat"])
            self.parking_store.set_boundary_lon(name, lot["boundary_long"])
            self.parking_store.set_type(name, lot["type"])
        self.__class__.parking_store = self.parking_store

    def create_app(self):
        global app
        app = Flask(__name__)
        from engine import engine
        app.register_blueprint(engine)
        app.debug = True
        app.config['SECRET_KEY'] = SECRET_KEY
        return app

app_instance = App()
app = app_instance.create_app()

if __name__ == '__main__':
    app.run()
