from twisted.internet import stdio, reactor, protocol
from twisted.protocols import basic
import re
import random

class DataForwardingProtocol(protocol.Protocol):
    def __init__(self, clients):
        self.clients = clients
        self.name = random.getrandombits(128)
        self.output = None
        self.normalizeNewlines = False

    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
        if self.output:
            self.output.write(data)
   
    def connectionLost(self, reason):
        #@todo 

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
        self.clients[inputForwarder.name] = inputForwarder 
        print "Connected to server.  Press ctrl-C to close connection."

class StdioProxyFactory(protocol.ClientFactory):
    protocol = StdioProxyProtocol
    
    def __init__(self):
        self.clients={}

    def buildProtocol(self, addr):
        return StdioProxyProtocol(self.clients)

    def clientConnectionLost(self, transport, reason):
        reactor.stop( )

    def clientConnectionFailed(self, transport, reason):
        print reason.getErrorMessage( )
        reactor.stop( )
