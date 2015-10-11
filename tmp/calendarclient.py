from twisted.internet import reactor, defer
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from sys import stdout

class CalendarClient(Protocol):
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\r\n" % msg)
        stdout.write("Send Message %s\n" % msg)

    def dataReceived(self, data):
        stdout.write("Data %s\n" % data)
        self.handle_user_input()

    def handle_user_input(self):
        userInput = raw_input(">>")
        self.sendMessage(userInput)

class CalendarClientFactory(ReconnectingClientFactory):
    def __init__(self):
        self.p = None

    def startedConnecting(self, connector):
        print 'Started to connect.'
  
    def buildProtocol(self, addr):
        print 'Connected.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        self.p = CalendarClient()
        return self.p

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)

reactor.connectTCP("52.26.113.118", 12345, CalendarClientFactory())
#@TODO connect to other nodes
reactor.run()
