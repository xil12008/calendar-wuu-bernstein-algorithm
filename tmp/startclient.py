#!/usr/bin/python

import threading
import time

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from sys import stdout

from calendarclient import CalendarClient, CalendarClientFactory 
from calendarserver import CalendarServer, CalendarServerFactory

reactor.connectTCP("52.26.113.118", 12345, CalendarClientFactory())
reactor.run()

