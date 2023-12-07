from coapthon.server.coap import CoAP
from SmartBus13Resource import SmartBus13Resource

class SmartBus13Server(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('SmartBus13/', SmartBus13Resource())

server = SmartBus13Server("localhost", 5686)
try:
    server.listen(10)
except KeyboardInterrupt:
    print("Server Shutdown")
    server.close()
    print("Exiting...")
