import sys
import json

from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.python import log
from twisted.internet import reactor


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        self.num_variants = 0
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        payload = 'getNextVariant'
        self.sendMessage(payload.encode('utf8'), False)

    def onMessage(self, payload, isBinary):
        payload = payload.decode('utf8')
        if payload == "finished": 
            self.sendClose()
            return
        print("{}".format(payload))
        self.num_variants += 1
        if self.num_variants % 1000 == 0: print(self.num_variants)
        payload = 'getNextVariant'
        self.sendMessage(payload.encode('utf8'), False)
        # normally you'd transform the variant back to json here 
        # and do something with it eg...
        #obj = json.loads(payload.decode('utf8'))
        #print("{}".format(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))))
        
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        print("{} variants transfered during session".format(self.num_variants))
        reactor.stop()


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()
