from twisted.internet import stdio, reactor, protocol
from twisted.protocols import basic
import re
import random

from calendarserver import CalendarServer, CalendarServerFactory

#         DataFowardingProtocolVV
#   user-----> inputForwarder       .output
#     <--                                 \-->-->--->>
#        \ .output                                    \ 
#       instance of stdioProxyProtocol     .transport--> remote server

class DataForwardingProtocol(protocol.Protocol):
    def __init__(self, clients):
        self.clients = clients
        self.name = random.getrandbits(128)
        self.output = None
        self.normalizeNewlines = False

    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
        if self.output:
            self.multicast(data)
           
    def multicast(self, data):
        self.output.write("channel%s: %s" %(self.name , data))
        for name, protocol in self.clients.iteritems():
            if protocol != self:
                protocol.output.write("channel%s: %s" %(protocol.name , data))

    def send2Node(self, nodeId, data):
        return

    def handlingUserInput(self, cmd):
        return
   
    def connectionMade(self):
        self.clients[self.name] = self 

    def connectionLost(self, reason):
        if self.name in self.clients:
            del self.clients[self.name]

class StdioProxyProtocol(protocol.Protocol):
    def __init__(self, clients):
        self.output = None
        self.clients = clients
        self.normalizeNewlines = False

    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
        if self.output:
            self.output.write(data)

    def connectionMade(self):
        inputForwarder = DataForwardingProtocol(self.clients)
        inputForwarder.output = self.transport
        inputForwarder.normalizeNewlines = True
        stdioWrapper = stdio.StandardIO(inputForwarder)
        self.output = stdioWrapper
        print "Connected to server.  Press ctrl-C to close connection."

class StdioProxyFactory(protocol.ClientFactory):
    protocol = StdioProxyProtocol
    
    def __init__(self, ID):
        #start one unique server
        reactor.listenTCP(12345, CalendarServerFactory())
        self.clients={}
        self.ID = ID 

    def buildProtocol(self, addr):
        return StdioProxyProtocol(self.clients)

    def clientConnectionLost(self, transport, reason):
        reactor.stop( )

    def clientConnectionFailed(self, transport, reason):
        print reason.getErrorMessage( )
        reactor.stop( )
