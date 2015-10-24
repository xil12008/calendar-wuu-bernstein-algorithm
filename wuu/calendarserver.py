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
import random
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


class CalendarServer(LineReceiver):
    def __init__(self, algorithm, node, users):
        self.algorithm = algorithm   
        self.node = node
        self.users = users

    def connectionMade(self):
        stdout.write("Connection Made from %s\n" \
                         % self.transport.getPeer())
        targetID = Configuration.getID(self.transport.getPeer().host)
        self.users[targetID] = self
        self.sendLine("Connection Made. Now, you could send me messages.")

    def connectionLost(self, reason):
        stdout.write("Connection Lost from %s\n" \
                         % self.transport.getPeer())
        targetID = Configuration.getID(self.transport.getPeer().host)
        if targetID in self.users:
            del self.users[targetID]

    def lineReceived(self, line):
        stdout.write("Server%d Received Data: %s\n" %( Configuration.getMyID(), line))
        delMsgs = self.algorithm.receiveMsg(line, self.node)
        #return the jsonmsg to various nodes 
        #send jsonmsg to nodes to notify them 
        #it's for conflicts
        #self.send2Node(0, "fake conflict notification")
        if delMsgs:
            for delMsg in delMsgs: 
                #put delete event into the log and execute delete
                e = self.node.createEvent(delMsg)
            for i in range(self.algorithm.n):#@TODO this line is broadcast  
                jsonmsg = self.algorithm.sendMsg2Node(i) 
                self.send2Node(i, jsonmsg)

    def send2Node(self, nodeId, data):
        for name, protocol in self.users.iteritems():
            if name == nodeId and nodeId != Configuration.getMyID(): 
                protocol.sendLine(data)
                return
        logging.warning("One server's message not reply to client because no connection found or it's itself.")

class CalendarServerFactory(Factory):
    def __init__(self, algorithm, node):
        self.algorithm = algorithm
        self.node = node
        self.users = {} 

    def buildProtocol(self, addr):
        return CalendarServer(self.algorithm, self.node, self.users)

