import sys
import json

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import google.protobuf.json_format as json_format
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.task import cooperate

import datamodel.variant
import ga4gh.variant_service_pb2 as variant_service_pb2

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        self.num_variants = 0
        print("Client connecting: {0}".format(request.peer))

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

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        print("{} variants sent".format(self.num_variants))


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    reactor.listenTCP(9000, factory)
    reactor.run()
