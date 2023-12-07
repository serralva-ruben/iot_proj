from coapthon.client.helperclient import HelperClient
from datetime import datetime, timedelta
import time

class Application:
    def __init__(self, server):
        self.server = server
        self.client = HelperClient(server=server)
        self.subscriptions = {}

    def subscribe_to_resource(self, resource):
        self.client.observe(resource, self.callback)

    def callback(self, response):
        print("Received notification from {}: {}".format(response.source, response.payload))
        if response.payload == "Bus":
            self.subscribe_to_bus(response.source)

    def subscribe_to_bus(self, bus):
        if bus not in self.subscriptions or datetime.now() - self.subscriptions[bus] > timedelta(minutes=10):
            self.client.observe(bus, self.callback)
            self.subscriptions[bus] = datetime.now()

    def run(self):
        self.subscribe_to_resource('ResDir2')
        while True:
            time.sleep(60)  # Sleep for 60 seconds

app = Application(("localhost", 5683))
app.run()
