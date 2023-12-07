from coapthon.resources.resource import Resource
from pymongo import MongoClient
from datetime import datetime, timedelta
import threading
import time

class SmartCar1Resource(Resource):
    def __init__(self, name="SmartCar1Resource", coap_server=None):
        super(SmartCar1Resource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "SmartCar1 Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"
        self.timestamp = datetime.now()
        self.vehicle_type = "Car"  # Or get this value from MongoDB

        # MongoDB setup
        self.client = MongoClient('localhost', 27017)  # Update with your MongoDB details
        self.db = self.client['iot_project']
        self.smartcar1_collection = self.db['smartcar1_collection']

    def render_GET(self, request):
        # Check if the resource representation has expired
        if datetime.now() - self.timestamp > timedelta(minutes=10):
            return None  # Or however you want to handle expired resources

        # Retrieve data from MongoDB and update the payload
        smartcar1_data = self.smartcar1_collection.find_one({"name": "SmartCar1"})
        if smartcar1_data:
            self.payload = "Location: {}".format(smartcar1_data.get("location", "Unknown"))
        return self

    def render_PUT(self, request):
        # Update the location of SmartCar1 in MongoDB based on the received payload
        new_location = request.payload
        self.smartcar1_collection.update_one({"name": "SmartCar1"}, {"$set": {"location": new_location}})
        self.timestamp = datetime.now()  # Update timestamp
        return self

    def render_POST(self, request):
        # Create a new SmartCar1 resource in MongoDB
        initial_details = request.payload
        self.smartcar1_collection.insert_one({"name": "SmartCar1", "details": initial_details, "location": "Unknown"})
        return self

    def render_DELETE(self, request):
        # Delete the SmartCar1 resource from MongoDB
        self.smartcar1_collection.delete_one({"name": "SmartCar1"})
        return True

smartcar1 = SmartCar1Resource()

def update_resource_value(resource):
    while True:
        # Update resource value here
        resource.payload = get_new_value()  # Replace with your own method to get a new value
        resource.updated_state()  # Notify observers about the change
        time.sleep(60)  # Sleep for 60 seconds

# Start a new thread that updates the resource value every 60 seconds
threading.Thread(target=update_resource_value, args=(smartcar1,)).start()
