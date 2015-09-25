#!/bin/python

'''
   This file is for configuration
'''

IP_Table = ['52.89.222.24','52.26.113.118']
PORT = 12345 #All nodes will use this port

def getIP(nodeID):
    if(nodeID >= len(IP_Table)): 
        print "Sorry, nodeID too large"
        return None
    return IP_Table[nodeID]

