# coding: utf-8
import subprocess
import os
import time
from datetime import datetime
import re

class Crontab:

    def create(self, date_time, jobid, action):
        dt=datetime.fromtimestamp(date_time)
        #print dt
        DD = dt.day
        MM = dt.month
        hh = dt.hour
        print hh
        mm = dt.minute
        ss = dt.second
        dayofweek = dt.isocalendar()[2]
        task = """%s %s %s %s %s sleep %s; /bin/python /home/thomson_crontab/start_job/thomson_job.py -j %s -s %s"""%(mm,hh,DD,MM,dayofweek,ss,jobid,action )
        return task

    def _runcmd(self, cmd, input=None):
        if input is not None:
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 close_fds=True, preexec_fn=os.setsid)
        else:
            p = subprocess.Popen(cmd, shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 close_fds=True, preexec_fn=os.setsid)

        stdoutdata, stderrdata = p.communicate(input)
        return p.returncode, stderrdata, stdoutdata

    # currently installed crontabs
    def get_list(self):
        retcode, err, installed_content = self._runcmd('crontab -l')
        if retcode != 0 and 'no crontab for' not in err:
            raise OSError('crontab not supported in your system')
        else:
            # merge the new crontab with the old one
            installed_content = installed_content.rstrip("\n")
            return installed_content

    def append(self, content='', override=False):
        if not content:
            raise ValueError('neither filename or crontab must be specified')
        if override:
            installed_content = ''
        else:
            installed_content =  self.get_list()
            #print installed_content
        installed_crontabs = installed_content.split('\n')
        for crontab in content.split('\n'):
            if crontab and crontab not in installed_crontabs:
                if not installed_content:
                    installed_content += crontab
                else:
                    installed_content += '\n%s' % crontab
            else:
                print 'New crontab was available'
        if installed_content:
            installed_content += '\n'
        # install back
        retcode, err, out = self._runcmd('crontab', installed_content)
        if retcode != 0: 
            raise ValueError('failed to install crontab, check if crontab is valid')

    def pop(self, content=''):
        if not content:
            raise ValueError('neither filename or crontab must be specified')
        else:
            content = content.strip()
        installed_content =  self.get_list()
        if not installed_content:
            return 'Crontab is not available'
        new_crontab = ''
        for old_crontab in installed_content.split('\n'):
            if old_crontab != content:
                new_crontab += '\n%s' % old_crontab
        if new_crontab:
            new_crontab += '\n'
        # install back
        retcode, err, out = self._runcmd('crontab', new_crontab)
        if retcode != 0: 
            raise ValueError('failed to install crontab, check if crontab is valid')
    
class ReadCrontab:
    def __init__(self, task):
        self.task = task
    def get_space_position(self, times):
        position = 0
        count = 0
        for i in self.task:
            if i == ' ':
                count += 1
                if count == times:
                    return position
            position +=1
        return -1

    def get_ss(self):
        return self.task[self.get_space_position(6): self.task.find('; ')]
    def get_mm(self):
        return self.task[0 : self.get_space_position(1)]
    def get_hh(self):
        return self.task[self.get_space_position(1) : self.get_space_position(2)]
    def get_dd(self):
        return self.task[self.get_space_position(2) : self.get_space_position(3)]
    def get_MM(self):
        return self.task[self.get_space_position(3) : self.get_space_position(4)]
    def get_day_of_week(self):
        return self.task[self.get_space_position(4) : self.get_space_position(5)]
    def get_job_id(self):
        return self.task[self.task.find('-j ')+3 : self.task.find('-s ')-1]
    def get_action(self):
        return self.task[self.task.find('-s ')+3 : len(self.task)]
    def get_all(self):
        number_pattern=re.compile("\d{1,2}")
        list_time=re.findall(number_pattern, self.task)
        print list_time
        ss = list_time[5]
        mm = list_time[0]
        hh = list_time[1]
        dd = list_time[2]
        MM = list_time[3]
        dayofweek = list_time[4]
        jid_pattern = re.compile("\d{4,10}")
        list_jid = re.findall(jid_pattern, self.task)
        jid = list_jid[0]
        a_pattern = re.compile("(?:-[Ss] [Ss]tart|-[Ss] [Ss]top)")
        print re.findall(a_pattern, self.task)
        return ss,mm,hh,dd,MM,dayofweek,jid
#Crontab().append(content='11 11 * * * /bin/sh /home/thomson_crontab/add_aa.sh', override=False)
#Crontab().pop(content='35 15 * * * /bin/sh /home/thomson_crontab/add_aa.sh')
#Crontab().append(Crontab().create(1508144477, '111111', 'start'))
#print Crontab().get_list()
print ReadCrontab('1 16 16 10 1 sleep 17; /bin/python /home/thomson_crontab/start_job/thomson_job.py -j 111111 -S Stop').get_all()
