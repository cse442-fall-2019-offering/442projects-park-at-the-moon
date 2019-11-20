import sys,os
import json
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from store import *
from config import SECRET_KEY

sys.path.append(os.getcwd() + '/patm-server')
app = None


class App:

    parking_store = None

    def __init__(self):

        self.parking_store = Store()

        data = None
        filename = os.getcwd() + '/patm-server/' + "data.json"
        if len(sys.argv) > 1 and sys.argv[1] == "local" or ("pytest" in sys.modules):
            filename = "data.json"
        with open(filename) as file:
            data = json.load(file)
        for lot in data['lots']:
                name = lot["name"]
                self.parking_store.add_lot(name, lot["capacity"], lot["boundary_lat"], lot["boundary_long"])
                self.parking_store.set_available_times(name, lot["available_times"])
                self.parking_store.set_type(name, lot["type"])
        for building in data['buildings']:
            self.parking_store.add_building(building)

        self.__class__.parking_store = self.parking_store
        self.global_history = GlobalHistory(self.parking_store)

    def create_app(self):
        global app
        app = Flask(__name__)
        from engine import engine
        app.register_blueprint(engine)
        app.debug = True
        app.config['SECRET_KEY'] = SECRET_KEY
        return app

    def update_status(self):
        print("updating", flush=True)
        self.global_history.update(self.parking_store, datetime.now())


app_instance = App()
app = app_instance.create_app()
scheduler = BackgroundScheduler()
scheduler.add_job(app_instance.update_status, 'interval', seconds = 30)
scheduler.start()

if __name__ == '__main__':
    app.run()
