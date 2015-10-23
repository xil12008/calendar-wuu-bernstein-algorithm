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

from db.db import DataConn 

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
    def __init__(self, name, node, time, content):
        self.name = name
        self.node = node
        self.time = time
        self.content = content
        logging.debug("Event %s created." % self.name)

class WBAlgorithm:
   def __init__(self):
       self.n = Configuration.getN()
       self.C = 0
       self.ID = Configuration.getMyID()
       self.dc = DataConn()


   #def __printMatrix(self):
   #    for i in range(self.n):
   #        for j in range(self.n):
   #            logging.debug("%d %d = %d" %( i, j, self.matrix[i][j]))
   #        logging.debug("---")
  
   def addEvent(self, event):
       return
       #self.dc.updateTime(event.node, event.node,event.time)
       #self.dc.addLog(event.name,event.node,event.time,event.content)
       #@TODO put the new event into database
   
   def __hasRec(self, matrix, event, k):
       logging.debug("__hasRec: k=%d event.node=%d" %(k, event.node))
       return matrix[k][event.node] >= event.time
 
   #Prepare the message to be send to node k  
   def sendMsg2Node(self, nodek):
       #@TODO load log from database
       log = self.dc.getLogs(0,sys.maxint)
       NP = {} #partial log
       ES = {} #event lists
       matrix =  [[0 for _ in range(self.n) ] for _ in range(self.n)]
       for i in range(self.n):
           for j in range(self.n):
               matrix[i][j] = self.dc.getTime(i, j)
       for (id,name,time,content) in log:
           event = Event(id,name,time,content)
           if not self.__hasRec(matrix, event, nodek):
              ES[event.name] = (event.time, event.node, event.content)  
              logging.debug((event.time, event.node, event.content))
       NP["matrix"] = matrix
       NP["events"] = ES 
       NP["senderID"] = Configuration.getMyID() 
       NP["receiverID"] = nodek 
       logging.debug(json.dumps(NP))
       return json.dumps(NP)
 
   def receiveMsg(self, jsonMsg):
       logging.debug("Received Json: %s" % jsonMsg)
       #@TODO merge log in database
       data = json.loads(jsonMsg)
       m = data["matrix"]
       events = data["events"]
       for key, value in events.iteritems():
           self.dc.addLog(key,value[1],value[0],value[2])
        
       matrix =  [[0 for _ in range(self.n) ] for _ in range(self.n)]
       for i in range(self.n):
           for j in range(self.n):
               matrix[i][j] = self.dc.getTime(i, j)
       for j in range(self.n):
           matrix[self.ID][j] = max( matrix[self.ID][j], m[data["senderID"]][j]) 
       for j in range(self.n):
           for k in range(self.n):  
               matrix[j][k] = max( matrix[j][k], m[j][k]) 
       for i in range(self.n):
           for j in range(self.n):
               self.dc.updateTime(i, j, matrix[i][j])

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
    node = Node()
    e1 = node.createEvent("whatever1")
    e2 = node.createEvent("whatever2")
    e3 = node.createEvent("whatever3")
    e4 = node.createEvent("whatever4")
    e5 = node.createEvent("whatever5")
    wb = WBAlgorithm()
    msg = wb.sendMsg2Node(0)
    wb.receiveMsg(msg)

class Node():
    dc = DataConn()
    node = Configuration.getMyID()
    def createEvent(self,content):
        name = random.getrandbits(5)
        time = self.dc.getTime(self.node,self.node)+1
        event = Event(name,self.node,time,content)
        self.dc.updateTime(self.node, self.node,time)
        self.dc.addLog(event.name,event.node,event.time,event.content)
        return event
