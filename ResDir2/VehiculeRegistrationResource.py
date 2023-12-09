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
        try:
            data = json.loads(request.payload)
            vehicle_id = data.get('vehicle_id')
            location = data.get('location')

            if not vehicle_id or not location:
                return self

            # Add a timestamp to the registration data
            data['timestamp'] = time.time()
            self.vehicle_registrations[vehicle_id] = data

            # MQTT Notification
            mqtt_topic = "vehicles/zone_a"
            mqtt_message = json.dumps({"vehicle_id": vehicle_id, "status": "entered_zone_a", "location": location})
            publish.single(mqtt_topic, payload=mqtt_message, hostname="localhost")

            self.payload = json.dumps({"message": f"Vehicle {vehicle_id} registered successfully"})
        except ValueError:
            self.payload = "Invalid JSON format"

        return self