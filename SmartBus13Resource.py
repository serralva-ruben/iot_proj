from coapthon.resources.resource import Resource
from pymongo import MongoClient
from datetime import datetime, timedelta
import threading
import time

class SmartBusResource(Resource):
    def __init__(self, bus_id, coap_server=None):
        super(SmartBusResource, self).__init__("SmartBus{}".format(bus_id), coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "SmartBus{} Resource".format(bus_id)
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"
        self.bus_id = bus_id
        self.timestamp = datetime.now()
        self.vehicle_type = "Bus"  # Or get this value from MongoDB

        # MongoDB setup
        self.client = MongoClient('localhost', 27017)  # Update with your MongoDB details
        self.db = self.client['iot_project']
        self.smartbus_collection = self.db['smartbus_collection']

    def render_GET(self, request):
        # Check if the resource representation has expired
        if datetime.now() - self.timestamp > timedelta(minutes=10):
            return None  # Or however you want to handle expired resources

        # Retrieve data from MongoDB and update the payload
        smartbus_data = self.smartbus_collection.find_one({"bus_id": self.bus_id})
        if smartbus_data:
            self.payload = "Location: {}".format(smartbus_data.get("location", "Unknown"))
        return self

    def render_PUT(self, request):
        # Update the location of the SmartBus in MongoDB based on the received payload
        new_location = request.payload
        self.smartbus_collection.update_one({"bus_id": self.bus_id}, {"$set": {"location": new_location}})
        self.timestamp = datetime.now()  # Update timestamp
        return self

    def render_POST(self, request):
        # Create a new SmartBus resource in MongoDB
        initial_details = request.payload
        self.smartbus_collection.insert_one({"bus_id": self.bus_id, "details": initial_details, "location": "Unknown"})
        return self

    def render_DELETE(self, request):
        # Delete the SmartBus resource from MongoDB
        self.smartbus_collection.delete_one({"bus_id": self.bus_id})
        return True

smartbus1 = SmartBusResource(1)
smartbus2 = SmartBusResource(2)

def update_resource_value(resource):
    while True:
        # Update resource value here
        resource.payload = get_new_value()  # Replace with your own method to get a new value
        resource.updated_state()  # Notify observers about the change
        time.sleep(60)  # Sleep for 60 seconds

# Start a new thread that updates the resource value every 60 seconds
threading.Thread(target=update_resource_value, args=(smartbus1,)).start()
threading.Thread(target=update_resource_value, args=(smartbus2,)).start()
