.. wuu documentation master file, created by
   sphinx-quickstart on Sat Sep 26 00:43:56 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Wuu-Bernstein-Algorithm-based Calendar's documentation!
=======================================================================

For this project, we will implement a distributed calendar application using a replicated log and dictionary. There are totally 4 nodes and every node could schedule appointments with others. 

Calendar will keep appointment event, where each appointment is a tuple consisting of the following fields:

1.Name: unique appointment name

2.Day: Date of appointment

3.Start Time

4.End Time

5.Participants: List of node ids

-----------------------------------------------
Wuu Bernstein Algorithm
-----------------------------------------------

The paper `paper link`_.

.. _paper link: http://cs.ucsb.edu/~hatem/cs271/replicated-log.pdf

Each node keeps a log, recording every local event, i.e. a new appointment been scheduled/deleted. Those local events are shared among nodes so that all the other nodes will be updated.

Each node also maintains a dictionary according to the events. If a node receives some new events from another node, then it will operate on its' own dictionary and try to keep dictionary up-to-date.
 
For example, node i schedule an appointment with node j, let's call this event E. node i puts E into its local log and send a message to notify node j. When j receives the message from i, it notices that, oops, new event E has not yet been executed yet, thus executes it, and this appointment event is inserted into j's dictionary. 

------------
Code:
------------
.. toctree::
   :maxdepth: 2

   code.rst

Github `github link`_.

.. _github link: https://github.com/xil12008/calendar-wuu-bernstein-algorithm 

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

