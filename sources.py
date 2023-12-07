import time
import json

from coapthon import defines

from coapthon.resources.resource import Resource

class SmartCar1(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(SmartCar1, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "Basic Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, SmartCar1())
        return res

    def render_DELETE(self, request):
        return True