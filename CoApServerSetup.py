from SmartBus13Resource import SmartBusResource
from SmartCar1Resource import SmartCar1Resource
from coapthon.server.coap import CoAP

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('SmartBus1/', SmartBusResource(1))
        self.add_resource('SmartBus2/', SmartBusResource(2))
        self.add_resource('SmartCar1/', SmartCar1Resource())

server = CoAPServer("localhost", 5683)
try:
    server.listen(10)
except KeyboardInterrupt:
    print("Server Shutdown")
    server.close()
    print("Exiting...")
