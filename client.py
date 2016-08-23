import sys
import json
from os import environ

from autobahn.wamp.types import CallOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

class Component(ApplicationSession):
    """
    Application component that consumes progressive results.
    """

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        self.num_variants = 0

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def on_progress(payload):
            print("{}".format(payload.decode('utf8')))
            self.num_variants += 1

        res = yield self.call(u'com.myapp.getVariants', options=CallOptions(on_progress=on_progress))

        print("Final: {}".format(res))
        self.leave()

    def onDisconnect(self):
        print("WebSocket connection closed")
        print("{} variants transfered during session".format(self.num_variants))
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://127.0.0.1:8080/ws",
                               realm=u"crossbardemo")
    runner.run(Component)
