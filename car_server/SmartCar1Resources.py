from coapthon.resources.resource import Resource
from geopy.geocoders import Nominatim
from coapthon.client.helperclient import HelperClient
import requests

ZONEA_Center = (49.612721712187586, 6.128316949370724) #ZONEA center coordinates
ZONEA_RADIUS = 5 #km

class SmartCar1Resources(Resource):
    def __init__(self, name="SmartCar1Resource", coap_server=None):
        super(SmartCar1Resources, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "SmartCar1 Initial Data"
        self.resource_type = "SmartCar1Resource"
        self.content_type = "text/plain"
        self.location = "Unknown"
        self.in_zone_a = False
        self.geolocator = Nominatim(user_agent="carResource")

    def render_GET(self, request):
        # Return the current state of the car
        self.payload = f"Location: {self.location}, In Zone A: {'Yes' if self.in_zone_a else 'No'}"
        return self

    def render_PUT(self, request):
        # Assuming the request payload is a dictionary
        self.location = request.payload.get('location', self.location)
        
        if is_inside_area(self.location, ZONEA_Center, ZONEA_RADIUS):
            self.in_zone_a = True
            self.update_resdir2(self.in_zone_a)
        else:
            self.in_zone_a = False

        self.payload = f"Updated Location: {self.location}, In Zone A: {'Yes' if self.in_zone_a else 'No'}"
        return self

    def update_resdir2(self, in_zone_a):
        if in_zone_a:
            registration_data = {
                "vehicle_id": self.name,
                "location": self.location,
            }

            try:
                client = HelperClient(server=('127.0.0.1', 5685))
                client.put("register", payload=str(registration_data), timeout=10)

            except Exception as e:
                print(f"Error communicating with ResDir2: {e}")

def is_inside_area(location, area_center, radius):
    R = 6371.0

    lat1 = radians(location[0])
    lon1 = radians(location[1])
    lat2 = radians(area_center[0])
    lon2 = radians(area_center[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance <= radius