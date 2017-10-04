# coding: utf-8
import subprocess
import os

class Crontab:

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
            print installed_content
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

Crontab().append(content='11 11 * * * /bin/sh /home/thomson_crontab/add_aa.sh', override=False)
#Crontab().pop(content='35 15 * * * /bin/sh /home/thomson_crontab/add_aa.sh')
