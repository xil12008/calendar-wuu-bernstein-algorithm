#!/bin/python
from urllib2 import urlopen

'''
   This file is for configuration
'''

class Configuration:
    IPTABLE = ['54.187.254.76','52.88.17.250']
    PORT = 12345 #All nodes will use this port
   
    def getPublicIP():
        return urlopen('http://ip.42.pl/raw').read()

    def getMyID():
        return getNodeID(urlopen('http://ip.42.pl/raw').read())
    
    def getNodeID(ip):
        for index, ele in enumerate(IPTABLE):
            if ele==ip:
                return index
    
    def getIP(nodeID):
        if(nodeID >= len(IP_Table)): 
            print "Sorry, nodeID too large"
            return None
        return IPTABLE[nodeID]
