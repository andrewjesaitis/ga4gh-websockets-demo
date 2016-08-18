import sys
import json

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import google.protobuf.json_format as json_format
from twisted.python import log
from twisted.internet import reactor

import datamodel.variant
import ga4gh.variant_service_pb2 as variant_service_pb2

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        self.num_variants = 0
        self.variantGenerator = self.variantPayloadGenerator('NCBI37', 0, 10000000)
        print("Client connecting: {0}".format(request.peer))

    def variantPayloadGenerator(self, reference_name, start, end):
        for rec in datamodel.variant.getPysamVariants(reference_name, '1', start, end):
            variant = datamodel.variant.convertVariant(rec, None)
            payload = json_format.MessageToJson(variant).encode('utf8')
            yield payload

    def onOpen(self):
        print("WebSocket connection open.")
        
    def onMessage(self, payload, isBinary):
        if self.num_variants % 1000 == 0: print(self.num_variants)
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            # print("Text message received: {0}".format(payload.decode('utf8')))
            payload = payload.decode('utf8')
            if payload == "getNextVariant":
                try:
                    payload = self.variantGenerator.next()
                    self.sendMessage(payload, False)
                    self.num_variants += 1
                except Exception as e:
                    print(e)
                    # No more variants
                    payload = 'finished'
                    self.sendMessage(payload.encode('utf8'), False)
            
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        print("{} variants sent".format(self.num_variants))


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    reactor.listenTCP(9000, factory)
    reactor.run()
