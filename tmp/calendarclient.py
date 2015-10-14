from twisted.internet import reactor, defer
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from sys import stdout

class CalendarClient(Protocol):
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\r\n" % msg)
        stdout.write("Send Message %s\n" % msg)

    def dataReceived(self, data):
        stdout.write("Data Received %s\n" % data)
        self.sendMessage(data)
        self.handle_user_input()

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
        stdio.StandardIO(self.p)
        return self.p

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)

