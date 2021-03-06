try:
    import asyncio
except ImportError:
    # Trollius >= 0.3 was renamed
    import trollius as asyncio

from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that subscribes and receives events, and
    stop after having received 5 events.
    """

    @asyncio.coroutine
    def onJoin(self, details):

        self.received = 0

        def on_event(i):
            print("Got event: {}".format(i))
            self.received += 1
            if self.received > 5:
                self.leave()

        yield self.subscribe(on_event, u'com.myapp.topic1')

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://api.poloniex.com"),
        u"crossbardemo",
    )
    runner.run(Component)