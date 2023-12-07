from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

class ResDirResource(Resource):
    def __init__(self, name="ResDir2", coap_server=None):
        super(ResDirResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "ResDir2 Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"
        self.vehicles = {}  # To store the vehicles that enter Zone A

    def render_GET(self, request):
        # Return the list of vehicles in Zone A
        self.payload = ", ".join(self.vehicles.keys())
        return self

    def render_PUT(self, request):
        # Update the list of vehicles in Zone A based on the received payload
        vehicle_name = request.payload
        self.vehicles[vehicle_name] = datetime.now()  # Update timestamp
        return self

class ResDirServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('ResDir2/', ResDirResource())

server = ResDirServer("localhost", 5684)
try:
    server.listen(10)
except KeyboardInterrupt:
    print("Server Shutdown")
    server.close()
    print("Exiting...")
