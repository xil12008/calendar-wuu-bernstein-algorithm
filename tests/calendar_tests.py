from nose.tools import *
import sys, os, pdb
sys.path = [os.path.abspath(os.path.dirname(__file__) + "/../calendar" )] + sys.path
import calendar 
import sampleclient

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"

def test_network():
    sampleclient.socketclient()
