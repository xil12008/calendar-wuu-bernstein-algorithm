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

class WBAlgorithm:
   def __init__(self):
       self.n = Configuration.getN()
       self.matrix =  [[] for _ in range(self.n)]

   def onAdd(self):
       pass 

   def onDelete(self):
       pass

   def notify(self):
       pass

   def onConflict(self):
       pass

   def onReceiveApp(self):
       pass

   def onRecover(self):
       pass
 
   def writeApp(self):
       pass
 
   def displayApp(self):
       pass


