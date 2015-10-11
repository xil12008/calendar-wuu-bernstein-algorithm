#!/usr/bin/python

import threading
import time

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from sys import stdout

from calendarclient import CalendarClient, CalendarClientFactory 
from calendarserver import CalendarServer, CalendarServerFactory

reactor.listenTCP(12345, CalendarServerFactory())
reactor.run()
