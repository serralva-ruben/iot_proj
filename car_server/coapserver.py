import getopt
import sys
from coapthon.server.coap import CoAP
from SmartCar1Resources import SmartCar1Resources

class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        self.add_resource('SmartCar1/', SmartCar1Resources(1))
        
        print("CoAP Server start on " + host + ":" + str(port))
        print(self.root.dump())


def usage():  # pragma: no cover
    print("coapserver.py -i <ip address> -p <port>")


def main(argv):  # pragma: no cover
    ip = "127.0.0.1"
    port = 5684
    multicast = False
    try:
        opts, args = getopt.getopt(argv, "hi:p:m", ["ip=", "port=", "multicast"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-m", "--multicast"):
            multicast = True

    server = CoAPServer(ip, port, multicast)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
