import time
from datetime import datetime
class Crontab:
    def __init__(self, date_time, jobid, action):
        self.date_time = date_time
        self.jid = jobid
        self.action = action

    def create(self):
        dt=datetime.fromtimestamp(self.date_time)
        print dt
        DD = dt.day
        MM = dt.month
        hh = dt.hour
        mm = dt.minute
        ss = dt.second
        dayofweek = dt.isocalendar()[2]
        task = """%s %s %s %s %s sleep %s; /bin/python /home/thomson_crontab/start_job/thomson_job.py -j %s -s %s"""%(mm,hh,DD,MM,dayofweek,ss,self.jid,self.action )
        return task

#1346236702
print Crontab(1507023742, '111111', 'start').create()
