import sys
import json
from os import environ

from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
import google.protobuf.json_format as json_format
from twisted.internet import reactor
from twisted.internet.task import cooperate

import datamodel.variant
import ga4gh.variant_service_pb2 as variant_service_pb2

class Component(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        self.num_variants = 0

    def sendVariants(self, reference_name, start, end):
        for rec in datamodel.variant.getPysamVariants(reference_name, '1', start, end):
            variant = datamodel.variant.convertVariant(rec, None)
            payload = json_format.MessageToJson(variant).encode('utf8')
            self.sendMessage(payload, isBinary = False)
            self.num_variants += 1
            yield None
        self.sendClose()  
      
    def onOpen(self):
        print("WebSocket connection open.")
        reference_name = 'NCBI37'
        start = 0
        end = 10000000
        cooperate(self.sendVariants(reference_name, start, end))

        yield self.register(getVariants, u'com.myapp.getVariants', RegisterOptions(details_arg='details'))

        print("procedures registered")

    def onLeave(self, details):
        print("Left connection: {0}".format(details))
        print("{} variants sent".format(self.num_variants))

if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://127.0.0.1:8080/ws",
                               realm=u"crossbardemo")
    
    runner.run(Component)
