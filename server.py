import sys
import json

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        self.num_variants = 0
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        
        test_variant = {"variant_id": "abc123"}
        payload = json.dumps(test_variant).encode('utf8')
        self.sendMessage(payload, isBinary = False)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        print("{} variants sent".format(self.num_variants))


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    reactor.listenTCP(9000, factory)
    reactor.run()
