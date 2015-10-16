"""
multicast.py
One Protocol connects to the local agent and other three to the three nodes.
Any data received from local agent will simplied be multicasted to all other nodes.

It's implemented based on Twisted.
"""

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from sys import stdout

from calendarclient import CalendarClient, CalendarClientFactory 
from calendarserver import CalendarServer, CalendarServerFactory
from proxyclient import StdioProxyFactory

class CalendarServer(LineReceiver):
    def __init__(self):
        spfactory =  StdioProxyFactory()
        reactor.connectTCP("52.88.17.250", 12345, spfactory)    

    def connectionMade(self):
        stdout.write("Connection Made from %s\n" \
                         % self.transport.getPeer())
        self.sendLine("Connection Made. Now, you could send me messages.")

    def connectionLost(self, reason):
        stdout.write("Connection Lost from %s\n" \
                         % self.transport.getPeer())

    def lineReceived(self, line):
        stdout.write("Received Data: %s\n" % line)

class CalendarServerFactory(Factory):
    def buildProtocol(self, addr):
        return CalendarServer()

