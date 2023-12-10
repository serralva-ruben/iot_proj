import json
from math import atan2, cos, radians, sin, sqrt
import certifi
import paho.mqtt.publish as publish
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, PyMongoError
import time

ZONEA_Center = (49.612721712187586, 6.128316949370724) #ZONEA center coordinates (Luxembourg ville)
ZONEA_RADIUS = 15 #km

class SmartBus13Resources(Resource):
    def __init__(self, name="SmartBus13Resource", coap_server=None):
        super(SmartBus13Resources, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.resource_type = "SmartBus13Resource"
        self.content_type = "application/json"
        self.location = "Unknown"
        self.in_zone_a = False
        self.mongo_client = self.initialize_mongo_client()

    def initialize_mongo_client(self):
        try:
            uri = "mongodb+srv://ruben:1234@cluster0.dlovykt.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
            # Test connection
            client.admin.command('ping')
            print("Connected to MongoDB successfully!")
            return client
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            return None

    def render_GET(self, request):
        self.payload = f"Location: {self.location}, In Zone A: {'Yes' if self.in_zone_a else 'No'}"
        return self

    def render_PUT(self, request):
        #converting request data from string to json
        try:
            request_payload = json.loads(request.payload)
        except json.JSONDecodeError:
            return self
        #print statement for debugging purposes
        print(f"payload: {request_payload}")
        #setting the attributes of the resource with the current bus data (name and location)
        self.name = request_payload["name"]
        self.location = {'lat':request_payload['lat'],'lon':request_payload['lon']}
        #register bus data inside mongo database
        if self.mongo_client:
            try:
                db = self.mongo_client['iot']
                collection = db['bus']
                data = {'name': self.name, 'location': self.location, 'timestamp': time.time()}
                collection.insert_one(data)
            except PyMongoError as e:
                print(f"MongoDB operation failed: {e}")
        #check wether bus is inside the are, if it is we call the 'update_resdit2' function and set in_zone_a to true, other wise to false
        if is_inside_area(self.location, ZONEA_Center, ZONEA_RADIUS):
            self.in_zone_a = True
            self.update_resdir2(self.in_zone_a)
        else:
            self.in_zone_a = False

        # send mqtt message with bus location
        mqtt_topic = "bus13/location"
        mqtt_message = json.dumps({"name": self.name, "status": "entered_zone_a", "location": json.dumps(self.location)})
        publish.single(mqtt_topic, payload=mqtt_message, hostname="localhost")

        return self

    def update_resdir2(self, in_zone_a):
        if in_zone_a:
            registration_data = {
                "vehicle_id": self.name,
                "location": self.location,
            }

            try:
                # Convert the registration data to a JSON string
                registration_data_json = json.dumps(registration_data)

                client = HelperClient(server=('127.0.0.1', 5685))
                response = client.put("register", payload=registration_data_json, timeout=10)
                print(f"Response from ResDir2: {response.pretty_print()}")
                client.stop()
            except Exception as e:
                print(f"Error communicating with ResDir2: {e}")

def is_inside_area(location, area_center, radius):
    R = 6371.0 #radius of earch in km

    lat1 = radians(location["lat"])
    lon1 = radians(location["lon"])
    lat2 = radians(area_center[0])
    lon2 = radians(area_center[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance <= radius