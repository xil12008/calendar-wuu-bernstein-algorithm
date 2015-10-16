from twisted.internet import stdio, reactor, protocol
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols import basic
import re
import random

from calendarserver import CalendarServer, CalendarServerFactory
from configure import Configuration

import pdb

import logging
import sys

LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }

if len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)


#         DataFowardingProtocolVV
#   user-----> inputForwarder       .output
#     <--                                 \-->-->--->>
#        \ .output                                    \ 
#       instance of stdioProxyProtocol     .transport--> remote server

class DataForwardingProtocol(protocol.Protocol):
    def __init__(self, clients, addr):
        self.clients = clients
        self.addr = addr
        self.IP = addr.host
        self.ID = Configuration.getID(self.IP)
        self.name = random.getrandbits(128)
        self.output = None
        self.normalizeNewlines = False

    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
        if self.output:
            self.multicast(data)
           
    def multicast(self, data):
        self.output.write("from%d: %s" %(self.ID, data))
        for name, protocol in self.clients.iteritems():
            if protocol != self:
                protocol.output.write("from%d: %s" %(self.ID, data))

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
    def __init__(self, clients, addr):
        self.output = None
        self.clients = clients
        self.addr = addr
        self.normalizeNewlines = False

    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
        if self.output:
            self.output.write(data)

    def connectionMade(self):
        inputForwarder = DataForwardingProtocol(self.clients, self.addr)
        inputForwarder.output = self.transport
        inputForwarder.normalizeNewlines = True
        stdioWrapper = stdio.StandardIO(inputForwarder)
        self.output = stdioWrapper
        logging.info("Client: Connected to server.  Press ctrl-C to close connection.")

class StdioProxyFactory(ReconnectingClientFactory):
    protocol = StdioProxyProtocol
    
    def __init__(self, ID, IP):
        #start one unique server
        reactor.listenTCP(12345, CalendarServerFactory())
        logging.info("Server%d Launched, my ip=%s" % (ID, IP))
        self.clients={}
        self.ID = ID 

    def buildProtocol(self, addr):
        #Consider expo delay for reconnection
        logging.info("Building Protocol addr=%s" % addr)
        return StdioProxyProtocol(self.clients, addr)
   
    def clientConnectionLost(self, connector, reason):
        logging.debug('Connection Lost. Reason: %s' % reason)
        logging.info('Connection Lost.') 
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.debug('Connection failed. Reason: %s' % reason)
        logging.info('Connection failed.') 
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)
