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
from configure import Configuration

class CalendarServer(LineReceiver):
    def __init__(self, algorithm, node):
        self.algorithm = algorithm   
        self.node = node

    def connectionMade(self):
        stdout.write("Connection Made from %s\n" \
                         % self.transport.getPeer())
        self.sendLine("Connection Made. Now, you could send me messages.")

    def connectionLost(self, reason):
        stdout.write("Connection Lost from %s\n" \
                         % self.transport.getPeer())

    def lineReceived(self, line):
        stdout.write("Server%d Received Data: %s\n" %( Configuration.getMyID(), line))
        self.algorithm.receiveMsg(line, self.node)

        #send jsonmsg to nodes to notify them 
        #it's for conflicts
        self.send2Node(0, "fake conflict notification")

    def send2Node(self, nodeId, data):
        for name, protocol in self.clients.iteritems():
            if protocol.targetID == nodeId:
                protocol.output.write("%s\r\n" %(data))
                return
        logging.warning("One message not sent because no connection found")


class CalendarServerFactory(Factory):
    def __init__(self, algorithm, node):
        self.algorithm = algorithm
        self.node = node

    def buildProtocol(self, addr):
        return CalendarServer(self.algorithm, self.node)

