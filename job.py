from optparse import OptionParser
import sys
import time
import re
import threading
from thomson_api import *
import MySQLdb as mdb
from config import *

# Parsing argurments
parser = OptionParser()
parser.add_option("-j", "-J", dest="jobid", type="string",
                  help="Job ID/list Job ID", metavar=' ')

parser.add_option("-s", "-S", dest="state", type="string",
                  help="State/ Action (start, stop,...)", metavar=' ')

parser.add_option("-n", "-N", dest="schedule_id", type="string",
                  help="Schedule id", metavar=' ')

(options, args) = parser.parse_args()

#Check argurments
for option in ('jobid', 'state'):
    if not getattr(options, option):
        print 'Option %s not specified' % option
        parser.print_help()
        sys.exit(0)

class Database:
    def __init__(self):
        self.db = NAME
        self.user = USER
        self.password = PASSWORD
        self.host = HOST
        self.port = PORT

    def connect(self):
        return mdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db)

    def close_connect(self, session):
        return session.close()

    def execute_query(self, query):
        if not query:
            print 'No query!'
            return 0
        session = self.connect()
        cur=session.cursor()
        cur.execute(query)
        session.commit()
        self.close_connect(session)
        return 1

def write_log(jobid, state, status):
    '''Create message here'''
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = "At %s Schedule %s jobid %s --> %s"%(now, state, jobid, status)
    '''pattern'''
    now = time.time()
    now_pattern = re.compile("\d+") 
    now = re.findall(now_pattern, str(now))
    now = now[0]
    host = THOMSON
    schedule_id = int(options.schedule_id) if options.schedule_id else None
    '''create query here'''
    if schedule_id:
        query="""insert into schedule_history(date_time, host, messages, schedule_id) values (%s, '%s', '%s', %d)"""%(now, host, message, schedule_id)
    else:
        query="""insert into schedule_history(date_time, host, messages) values (%s, '%s', '%s')"""%(now, host, message)
    return Database().execute_query(query)

jobid_pattern=re.compile("\d{3,10}")
list_jobid=re.findall(jobid_pattern, options.jobid)

def call_job(jobid, state):
    status = JobDetail(jobid).send_action(state)
    print "%s %s --> %s"%(state, jobid, status)
    try:
        write_log(jobid, state, status)
    except Exception as e:
        return 0
    return 1

list_t=[]
for jobid in list_jobid:
    t = threading.Thread(target=call_job, args=(jobid,options.state,))
    list_t.append(t)

'''start list job'''
for t in list_t:
    t.start()

'''wait for list job finish'''
for t in list_t:
    t.join()

