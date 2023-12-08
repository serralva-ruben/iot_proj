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
        self.location = request.payload.get('location', self.location)
        new_in_zone_a = request.payload.get('in_zone_a', self.in_zone_a)
        
        if new_in_zone_a != self.in_zone_a:
            self.in_zone_a = new_in_zone_a
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