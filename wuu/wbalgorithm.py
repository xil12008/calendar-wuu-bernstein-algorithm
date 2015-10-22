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
import json

import random

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

class Event:
    def __init__(self, name, time, node, content):
        self.name = random.getrandbits(128) #Name of the event
        self.time = 1 #@TODO get the newest Lamport timestamp
        self.node = Configuration.getMyID()  # where an event occurs
        self.content = content
        logging.debug("Event %s created." % self.name)

class WBAlgorithm:
   def __init__(self):
       self.n = Configuration.getN()
       self.matrix =  [[0 for _ in range(self.n) ] for _ in range(self.n)]
       self.C = 0
       self.ID = Configuration.getMyID()
       self.log = []

   def __printMatrix(self):
       for i in range(self.n):
           for j in range(self.n):
               logging.debug("%d %d = %d" %( i, j, self.matrix[i][j]))
           logging.debug("---")
  
   def addEvent(self, event):
       self.log.append(event)
       #@TODO put the new event into database
   
   def __hasRec(self, event, k):
       logging.debug("k=%d event.node=%d" %(k, event.node))
       return self.matrix[k][event.node] >= event.time
 
   #Prepare the message to be send to node k  
   def sendMsg2Node(self, nodek):
       #@TODO load log from database
       NP = {} #partial log
       #@TODO load log from database
       for event in self.log:
           if not self.__hasRec(event, nodek):
              NP[event.name] = (event.time, event.node, event.content)  
              logging.debug((event.time, event.node, event.content))
       NP["matrix"] = self.matrix
       NP["senderID"] = Configuration.getMyID() 
       logging.debug(json.dumps(NP))
       return json.dumps(NP)
 
   def receiveMsg(self, jsonMsg):
       logging.debug("Received Json: %s" % jsonMsg)
       #@TODO merge log in database
       data = json.loads(jsonMsg)
       m = data["matrix"] 
       for j in range(self.n):
           self.matrix[self.ID][j] = max( self.matrix[self.ID][j], m[self.ID][j]) 
       for j in range(self.n):
           for k in range(self.n):  
                self.matrix[j][k] = max( self.matrix[j][k], m[j][k]) 
       self.__printMatrix()

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

def test():
    e1 = Event("name1", 1, Configuration.getMyID(), "content1")
    e2 = Event("name2", 2, Configuration.getMyID(), "content2")
    e3 = Event("name3", 3, Configuration.getMyID(), "content3")
    e4 = Event("name4", 4, Configuration.getMyID(), "content4")
    e5 = Event("name5", 5, Configuration.getMyID(), "content5")
    wb = WBAlgorithm()
    wb.addEvent(e1)
    wb.addEvent(e2)
    wb.addEvent(e3)
    wb.addEvent(e4)
    wb.addEvent(e5)
    msg = wb.sendMsg2Node(0)
    wb.receiveMsg(msg)

test()
