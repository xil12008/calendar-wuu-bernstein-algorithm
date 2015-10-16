#!/usr/bin/python
import MySQLdb

class DataConn():
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
        user="root", # your username
        passwd="", # your password
        db="ds") # name of the data base

    def addLog(self, time_stamp, event_type, app_name):
        add_log = ("INSERT INTO logs "
            "(time_stamp, event_type, app_name) "
            "VALUES (%s, %s, %s)")
        data_log = (time_stamp, event_type, app_name)
        
        cur = self.db.cursor()
        cur.execute(add_log,data_log)
        self.db.commit()
        cur.close()
    
    def getLogs(self, start_stamp, end_stamp):
        cur = self.db.cursor()
        query = ("SELECT time_stamp, event_type, app_name FROM logs "
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
        cur.close()
        return time

    def updateTime(self, node0, node1, time):
        cur = self.db.cursor()
        query = ("UPDATE time SET node%s=%s WHERE node_id=%s")
        data_time = (node1, time, node0)
        cur.execute(query,data_time)
        cur.close()


def Test():
    dc = DataConn()
    dc.addLog(0,1,'test2')
    dc.addLog(1,1,'test2')
    dc.addLog(2,1,'test2')
    dc.addLog(3,1,'test2')
    dc.addLog(4,1,'test2')
    logs = dc.getLogs(1,3)
    for (time_stamp, event_type, app_name) in logs:
        print (time_stamp, event_type, app_name)
    
    dc.addApp('test', 1, 0, 1, '1 2')
    dc.addApp('test2', 1, 2, 4, '2 3')
    dc.addApp('test3', 1, 2, 4, '3 4')
    dc.delApp('test2')
    apps = dc.getApps()
    for (app_name, day, start_time, end_time, participants) in apps:
        print (app_name, day, start_time, end_time, participants)
    
    dc.initTime()
    dc.updateTime(0,1,3)
    time = dc.getTime(0,1)
    print time

    dc.db.close()

