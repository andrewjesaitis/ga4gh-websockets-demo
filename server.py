import sys
import json
from os import environ

from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
import google.protobuf.json_format as json_format
from twisted.internet import reactor
from twisted.python import log
from twisted.internet.defer import inlineCallbacks, returnValue

import datamodel.variant
import ga4gh.variant_service_pb2 as variant_service_pb2

class Component(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        self.num_variants = 0

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        @inlineCallbacks
        def getVariants(details=None):
            reference_name = 'NCBI37'
            start = 0
            end = 100000#00
            for rec in datamodel.variant.getPysamVariants(reference_name, '1', start, end):
                variant = datamodel.variant.convertVariant(rec, None)
                payload = json_format.MessageToJson(variant).encode('utf8')
                self.num_variants += 1
                details.progress(payload)
                yield True
            returnValue(True)
            self.sendClose()

        yield self.register(getVariants, u'com.myapp.getVariants', RegisterOptions(details_arg='details'))

        print("procedures registered")

    def onLeave(self, details):
        print("Left connection: {0}".format(details))
        print("{} variants sent".format(self.num_variants))

if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://127.0.0.1:8080/ws",
                               realm=u"crossbardemo")
    
    runner.run(Component)
