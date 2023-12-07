from coapthon.server.coap import CoAP
from SmartCar1Resource import SmartCar1Resource

class SmartCar1Server(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('SmartCar1/', SmartCar1Resource())

server = SmartCar1Server("localhost", 5685)
try:
    server.listen(10)
except KeyboardInterrupt:
    print("Server Shutdown")
    server.close()
    print("Exiting...")
