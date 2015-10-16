#!/usr/bin/python
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from sys import stdout

from proxyclient import StdioProxyFactory

from configure import Configuration 

#reactor.connectTCP("52.26.113.118", 12345, CalendarClientFactory())

#Note only creation once
spfactory =  StdioProxyFactory(Configuration.getMyID())
for ip in Configuration.IPTABLE:
    reactor.connectTCP(ip, Configuration.PORT, spfactory)
reactor.run()

