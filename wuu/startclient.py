#!/usr/bin/python
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from sys import stdout

from proxyclient import StdioProxyFactory

from configure import Configuration 

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

#Note only creation once
spfactory =  StdioProxyFactory(Configuration.getMyID(), Configuration.getPublicIP())
for ip in Configuration.IPTABLE:
    reactor.connectTCP(ip, Configuration.PORT, spfactory)
reactor.run()

