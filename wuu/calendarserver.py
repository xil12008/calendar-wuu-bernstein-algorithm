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
        self.users[Configuration.getID(self.transport.getPeer())] = self
        self.sendLine("Connection Made. Now, you could send me messages.")

    def connectionLost(self, reason):
        stdout.write("Connection Lost from %s\n" \
                         % self.transport.getPeer())
        if Configuration.getID(self.transport.getPeer()) in self.users:
            del self.users[Configuration.getID(self.transport.getPeer())]

    def lineReceived(self, line):
        stdout.write("Server%d Received Data: %s\n" %( Configuration.getMyID(), line))
        self.algorithm.receiveMsg(line, self.node)

        #send jsonmsg to nodes to notify them 
        #it's for conflicts
        self.send2Node(0, "fake conflict notification")

    def send2Node(self, nodeId, data):
        for name, protocol in self.users.iteritems():
            if name == nodeId:
                protocol.sendLine(data)
                return
        logging.warning("One server's message not reply to client because no connection found")

class CalendarServerFactory(Factory):
    def __init__(self, algorithm, node):
        self.algorithm = algorithm
        self.node = node
        self.users = {} 

    def buildProtocol(self, addr):
        return CalendarServer(self.algorithm, self.node, self.users)

