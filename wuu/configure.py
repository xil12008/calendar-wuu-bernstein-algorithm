#!/bin/python
from urllib2 import urlopen

'''
   This file is for configuration
'''

class Configuration:
    IPTABLE = ['52.89.158.138','52.88.245.160','54.175.50.224','52.71.252.179']
    PORT = 12345 #All nodes will use this port
  
    @staticmethod
    def getN():
        return len(Configuration.IPTABLE)

    @staticmethod 
    def getPublicIP():
        return urlopen('http://ip.42.pl/raw').read()

    @staticmethod 
    def getMyID():
        return Configuration.getID(urlopen('http://ip.42.pl/raw').read())
    
    @staticmethod 
    def getID(ip):
        for index, ele in enumerate(Configuration.IPTABLE):
            if ele==ip:
                return index
    
    @staticmethod 
    def getIP(nodeID):
        if(nodeID >= len(Configuration.IP_Table)): 
            print "Sorry, nodeID too large"
            return None
        return Configuration.IPTABLE[nodeID]
