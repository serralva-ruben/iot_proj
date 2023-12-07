from coapthon import defines
from coapthon.resources.resource import Resource
from pymongo import MongoClient

class SmartCar1Resource(Resource):
    def __init__(self, name="SmartCar1Resource", coap_server=None):
        super(SmartCar1Resource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "SmartCar1 Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

        # MongoDB setup
        self.client = MongoClient('localhost', 27017)  # Update with your MongoDB details
        self.db = self.client['iot_project']
        self.smartcar1_collection = self.db['smartcar1_collection']

    def render_GET(self, request):
        # Retrieve data from MongoDB and update the payload
        # For simplicity, let's assume a field 'location' in the MongoDB document
        # that stores the current location of SmartCar1
        smartcar1_data = self.smartcar1_collection.find_one({"name": "SmartCar1"})
        if smartcar1_data:
            self.payload = "Location: {}".format(smartcar1_data.get("location", "Unknown"))
        return self

    def render_PUT(self, request):
        # Update the location of SmartCar1 in MongoDB based on the received payload
        # For simplicity, let's assume the payload contains the new location
        new_location = request.payload
        self.smartcar1_collection.update_one({"name": "SmartCar1"}, {"$set": {"location": new_location}})
        return self

    def render_POST(self, request):
        # Create a new SmartCar1 resource in MongoDB
        # For simplicity, let's assume the payload contains initial details
        initial_details = request.payload
        self.smartcar1_collection.insert_one({"name": "SmartCar1", "details": initial_details, "location": "Unknown"})
        return self

    def render_DELETE(self, request):
        # Delete the SmartCar1 resource from MongoDB
        self.smartcar1_collection.delete_one({"name": "SmartCar1"})
        return True
