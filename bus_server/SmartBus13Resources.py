from coapthon.resources.resource import Resource
import requests

class SmartBus13Resources(Resource):
    def __init__(self, name="SmartBus13Resource", coap_server=None):
        super(SmartBus13Resources, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "SmartBus13 Initial Data"
        self.resource_type = "SmartBus13Resource"
        self.content_type = "text/plain"
        self.location = "Unknown"
        self.in_zone_a = False

    def render_GET(self, request):
        # Return the current state of the bus
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

            try:
                client = HelperClient(server=('127.0.0.1', 5683))
                client.put("register", payload=str(registration_data), timeout=10)

            except Exception as e:
                print(f"Error communicating with ResDir2: {e}")