from coapthon.resources.resource import Resource
from geopy.geocoders import Nominatim
from coapthon.client.helperclient import HelperClient

ZONEA_NAME = 'Canton Luxembourg'

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
        self.location = geolocator.reverse(request.payload.get('location', self.location))
        
        if self.location.address.split(",")[4].strip()==ZONEA_NAME:
            self.in_zone_a = True
            self.update_resdir2(self.in_zone_a)

        self.payload = f"Updated Location: {self.location}, In Zone A: {'Yes' if self.in_zone_a else 'No'}"
        return self

    def update_resdir2(self, in_zone_a):
        if in_zone_a:
            registration_data = {
                "vehicle_id": self.name,
                "location": self.location,
            }
            # URL of the ResDir2 registration endpoint
            resdir2_url = "http://127.0.0.1:5000/register"
            try:
                response = requests.put(resdir2_url, json=registration_data)
                if response.status_code == 200:
                    print(f"Successfully registered {self.name} to ResDir2")
                else:
                    print(f"Failed to register {self.name} to ResDir2: {response.text}")
            except requests.RequestException as e:
                print(f"Error communicating with ResDir2: {e}")
