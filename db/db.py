#!/usr/bin/python
import MySQLdb

class DataConn():
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
        user="root", # your username
        passwd="", # your password
        db="ds") # name of the data base

    def addLog(self, id, node, time_stamp, log):
        add_log = ("INSERT IGNORE INTO logs "
            "(id, node, time_stamp, log) "
            "VALUES (%s,%s, %s, %s)")
        data_log = (id, node, time_stamp, log)
        
        cur = self.db.cursor()
        cur.execute(add_log,data_log)
        self.db.commit()
        cur.close()
    
    def getLogs(self, start_stamp, end_stamp):
        cur = self.db.cursor()
        query = ("SELECT id, node, time_stamp, log FROM logs "
            "WHERE time_stamp >= %s AND time_stamp <= %s ")
        cur.execute(query,(start_stamp,end_stamp))
        logs = cur.fetchall()
        cur.close()
        return logs

    def addApp(self, app_name, day, start_time, end_time, participants):
        add_app = ("INSERT INTO appointments "
            "(app_name, day, start_time, end_time, participants) "
            "VALUES (%s, %s, %s, %s, %s)")
        data_app = (app_name, day, start_time, end_time, participants)

        cur = self.db.cursor()
        cur.execute(add_app,data_app)
        self.db.commit()
        cur.close()

    def getApps(self):
        cur = self.db.cursor()
        query = ("SELECT app_name, day, start_time, end_time, participants FROM appointments ")
        cur.execute(query)
        apps = cur.fetchall()
        cur.close()
        return apps
  
    def delApp(self, app_name):
        del_app = ("DELETE FROM appointments "
            "WHERE app_name = %s ")
        data_app = (app_name)

        cur = self.db.cursor()
        cur.execute(del_app,data_app)
        self.db.commit()
        cur.close()

    def getParticip(self, day, start_time, end_time):
        cur = self.db.cursor()
        query = ("SELECT participants FROM appointments "
            "WHERE day = %s AND start_time >= %s AND end_time <=%s ")
        data = (day, start_time, end_time)
        cur.execute(query,data)
        particip = cur.fetchall()
        cur.close()
        return particip

    def initTime(self):
        init_time = ("INSERT INTO time "
            "(node_id, node0, node1, node2, node3) "
            "VALUES (%s,%s, %s, %s, %s)")
        node0 = (0,0,0,0,0)
        node1 = (1,0,0,0,0)
        node2 = (2,0,0,0,0)
        node3 = (3,0,0,0,0)

        cur = self.db.cursor()
        cur.execute(init_time, node0)
        cur.execute(init_time, node1)
        cur.execute(init_time, node2)
        cur.execute(init_time, node3)
        self.db.commit()
        cur.close()

    def getTime(self, node0, node1):
        cur = self.db.cursor()
        query = ("SELECT node%s FROM time "
            "WHERE node_id = %s")
        cur.execute(query,(node1, node0))
        (time,) = cur.fetchone()
        self.db.commit()
        cur.close()
        return time

    def updateTime(self, node0, node1, time):
        cur = self.db.cursor()
        query = ("UPDATE time SET node%s=%s WHERE node_id=%s")
        data_time = (node1, time, node0)
        cur.execute(query,data_time)
        self.db.commit()
        cur.close()


def Test():
    dc = DataConn()
    dc.addLog(1, 1,0,'add play Sun 10:00am 1:00pm 1,2')
    dc.addLog(1, 1,1,'add play Sun 10:00am 1:00pm 1,3')
    dc.addLog(2, 3,2,'view')
    dc.addLog(3, 4,3,'del play')
    dc.addLog(4, 1,4,'sxx')
    logs = dc.getLogs(1,3)
    for event in logs:
        print event
    
    dc.addApp('test', 1, 0, 1, '1 2')
    dc.addApp('test2', 1, 2, 4, '2 3')
    dc.addApp('test3', 1, 2, 4, '3 4')
    particip = dc.getParticip(1, 2, 4)
    for (nodes,) in particip:
        print "particip:\t"
        print nodes

    dc.delApp('test2')
    apps = dc.getApps()
    for (app_name, day, start_time, end_time, participants) in apps:
        print (app_name, day, start_time, end_time, participants)
    
    dc.updateTime(0,1,3)
    time = dc.getTime(0,1)
    print time

    dc.db.close()

