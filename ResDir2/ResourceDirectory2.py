from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
import json
import time
import paho.mqtt.publish as publish
from VehiculeRegistrationResource import VehicleRegistrationResource

class ResDir2CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        vehicle_registration_resource = VehicleRegistrationResource(coap_server=self)
        self.add_resource('register/', vehicle_registration_resource)

def main():
    server = ResDir2CoAPServer("0.0.0.0", 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == '__main__':
    main()