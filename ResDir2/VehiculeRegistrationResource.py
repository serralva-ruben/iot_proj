from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
import json
import time
import paho.mqtt.publish as publish

class VehicleRegistrationResource(Resource):
    def __init__(self, name="VehicleRegistrationResource", coap_server=None):
        super(VehicleRegistrationResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "Vehicle Registration Resource"
        self.content_type = "application/json"
        self.vehicle_registrations = {}

    def render_PUT(self, request):
        print(self.vehicle_registrations)
        print('registering')
        try:
            data = json.loads(request.payload)
            vehicle_id = data.get('vehicle_id')
            location = data.get('location')

            if not vehicle_id or not location:
                return self

            current_time = time.time()
            data['timestamp'] = current_time
            self.vehicle_registrations[current_time] = data

            self.cleanup_registrations(current_time)

            # send mqtt message to client notifying that the vehicle entered the zone A
            mqtt_topic = "vehicles/zone_a"
            mqtt_message = json.dumps({"vehicle_id": vehicle_id, "status": "entered_zone_a"})
            publish.single(mqtt_topic, payload=mqtt_message, hostname="localhost")

            self.payload = json.dumps({"message": f"Vehicle {vehicle_id} registered successfully"})
        except ValueError:
            self.payload = "Invalid JSON format"

        return self
    
    def cleanup_registrations(self, current_time):
        ten_minutes_ago = current_time - 600  # 600 seconds = 10 minutes
        keys_to_delete = [key for key, value in self.vehicle_registrations.items() if value['timestamp'] < ten_minutes_ago]
        for key in keys_to_delete:
            del self.vehicle_registrations[key]