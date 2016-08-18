import sys

from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.python import log
from twisted.internet import reactor


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        self.num_variants = 0
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        self.num_variants += 1
        print("{}".format(payload.decode('utf8')))
        # normally you'd transform the variant back to json here 
        # and do something with it

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        print("{} variants transfered during session".format(self.num_variants))


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()
