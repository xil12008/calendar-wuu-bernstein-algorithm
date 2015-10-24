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
 
   def receiveMsg(self, jsonMsg, node):
       logging.debug("Received Json: %s" % jsonMsg)
       #@TODO merge log in database
       data = json.loads(jsonMsg)
       m = data["matrix"]
       events = data["events"]

       #fetch from local database
       matrix =  [[0 for _ in range(self.n) ] for _ in range(self.n)]
       for i in range(self.n):
           for j in range(self.n):
               matrix[i][j] = self.dc.getTime(i, j)

       #events ranked by target node's lamport timestamp
       eventslist = [] 
       for key, value in events.iteritems():
           #value[0:3] is (event.time, event.node, event.content)  
           #               ele[0]      ele[1]      ele[2]
           eventslist.append((value[0], value[1], value[2], key))
       rankedevents = sorted(eventslist) 
       for ele in rankedevents:
                 #Event(name, node, time, content)
           event = Event(key, ele[1], ele[0], ele[2])
           if not self.__hasRec(matrix, event, self.ID):
                   self.dc.addLog(ele[3],ele[1],ele[0],ele[2])
                   node.appOperation(ele[2]) #execute the operation
        
       #NOTE: matrix should be updated AFTER above events has been executed.
       for j in range(self.n):
           matrix[self.ID][j] = max( matrix[self.ID][j], m[data["senderID"]][j]) 
       for j in range(self.n):
           for k in range(self.n):  
               matrix[j][k] = max( matrix[j][k], m[j][k]) 
       for i in range(self.n):
           for j in range(self.n):
               self.dc.updateTime(i, j, matrix[i][j])

   def onAdd(self):
       #Insert an appointment
       #@TODO check conflict locally
       #
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
    e1 = node.createEvent("add|play|0|10|20|0,1,2,3")
    e2 = node.createEvent("add|play2|0|10|20|0,1,2,3")
    #e3 = node.createEvent("del|play")
    e4 = node.createEvent("whatever4")
    e5 = node.createEvent("whatever5")
    wb = WBAlgorithm()
    msg = wb.sendMsg2Node(0)

class Node():
    dc = DataConn()
    node = Configuration.getMyID()
    def createEvent(self,content):
        name = random.getrandbits(30)
        time = self.dc.getTime(self.node,self.node)+1
        event = Event(name,self.node,time,content)
        self.dc.updateTime(self.node, self.node,time)
        self.dc.addLog(event.name,event.node,event.time,event.content)
        self.appOperation(content)
        return event
    def appOperation(self,content):
        lists = content.split("|")
        if len(lists)==6 and lists[0]=="add":
            app_name = lists[1]
            app_day = lists[2]
            start_time = lists[3]
            end_time = lists[4]
            participants = lists[5]
            conflict = False
            preParticipants = self.dc.getParticip(app_day,start_time,end_time)
            for (users,) in preParticipants:
                if conflict == True: break
                for user in users.split(","):
                    if user == str(self.node):
                        conflict = True
                        break
                        
            self.dc.addApp(app_name,app_day,start_time,end_time, participants)
            if conflict==True :
                self.createEvent("del|"+app_name) 

        elif len(lists)==2 and lists[0]=="del":
            app_name = lists[1]
            self.dc.delApp(app_name)

    def viewApps(self):
        result = self.dc.getApps() 
        return result

