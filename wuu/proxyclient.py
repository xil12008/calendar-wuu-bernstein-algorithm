from twisted.internet import stdio, reactor, protocol
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols import basic
import re
import random

from calendarserver import CalendarServer, CalendarServerFactory
from configure import Configuration
from tmp_wbalgorithm import WBAlgorithm

import pdb

import logging
import sys

from ui.view import View

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
    def __init__(self, clients, algorithm, addr):
        self.clients = clients
        self.addr = addr
        self.IP = addr.host
        self.targetID = Configuration.getID(self.IP)
        self.name = random.getrandbits(128)
        self.output = None
        self.normalizeNewlines = False
        self.algorithm = algorithm 

    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
        if self.output:
            self.handleUserInput(data)
            #self.send2Node(1,data)
            #self.multicast(data)
           
    def multicast(self, data):
        self.output.write("%s" %(data))
        for name, protocol in self.clients.iteritems():
            if protocol != self:
                protocol.output.write("%s" %(data))
        #Unreliabe: without any check 

    def send2Node(self, nodeId, data):
        for name, protocol in self.clients.iteritems():
            if protocol.targetID == nodeId:
                protocol.output.write("%s" %(data))
                return
        logging.warning("One message not sent because no connection found")

    def handleUserInput(self, cmd):
        view = View()
        cmds = cmd.strip().split()
        if cmds[0]=="add":
            pdb.set_trace()
            if len(cmds)!=6:
                warning = "format: add <calendar name> <day> <start time> <end time> <participant list>"
                logging.warning(warning)
                return
            msg = cmds[0] +cmds[1] \
                  +str(view.days_int(cmds[2])) \
                  +str(view.time_int(cmds[3])) \
                  +str(view.time_int(cmds[4])) \
                  +cmds[5]

            self.transport.write(msg)
            for i in range(self.algorithm.n):
                jsonmsg = self.algorithm.sendMsg2Node(msg, i) 
                send2Node(i, jsonmsg)
        elif cmds[0]=="del":
            if len(cmds)!=2:
                warning = "format: del <calendar name>"
                logging.warning(warning)
                return
            self.transport.write(cmds[0]+cmds[1])
        elif cmds[0]=="view":
            self.transport.write(cmds[0])
   
    def connectionMade(self):
        self.clients[self.name] = self 

    def connectionLost(self, reason):
        if self.name in self.clients:
            del self.clients[self.name]

class StdioProxyProtocol(protocol.Protocol):
    def __init__(self, clients, algorithm, addr):
        self.output = None
        self.clients = clients
        self.addr = addr
        self.normalizeNewlines = False
        self.algorithm = algorithm 

    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
        if self.output:
            self.output.write(data)

    def connectionMade(self):
        inputForwarder = DataForwardingProtocol(self.clients, self.algorithm, self.addr)
        inputForwarder.output = self.transport
        inputForwarder.normalizeNewlines = True
        stdioWrapper = stdio.StandardIO(inputForwarder)
        self.output = stdioWrapper
        logging.info("Client: Connected to server.  Press ctrl-C to close connection.")

class StdioProxyFactory(ReconnectingClientFactory):
    protocol = StdioProxyProtocol
    
    def __init__(self, myID, IP):
        self.algorithm = WBAlgorithm()
        #start one unique server
        reactor.listenTCP(12345, CalendarServerFactory(self.algorithm))
        logging.info("Server%d Launched, my ip=%s" % (myID, IP))
        self.clients={}

    def buildProtocol(self, addr):
        #Consider expo delay for reconnection
        logging.info("Building Protocol addr=%s" % addr)
        return StdioProxyProtocol(self.clients, self.algorithm, addr)
   
    def clientConnectionLost(self, connector, reason):
        logging.debug('One Connection Lost. Reason: %s' % reason)
        logging.info('One Connection Lost.') 
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.debug('One Connection failed. Reason: %s' % reason)
        logging.info('One Connection failed.') 
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)
