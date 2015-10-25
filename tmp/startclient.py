#!/usr/bin/python

import threading
import time

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from sys import stdout

from calendarclient import CalendarClient, CalendarClientFactory 
from calendarserver import CalendarServer, CalendarServerFactory
from proxyclient import StdioProxyFactory

#reactor.connectTCP("52.26.113.118", 12345, CalendarClientFactory())

spfactory =  StdioProxyFactory()
reactor.connectTCP("52.89.158.138", 12345, spfactory)
reactor.connectTCP("52.88.245.160", 12345, spfactory)

reactor.run()

