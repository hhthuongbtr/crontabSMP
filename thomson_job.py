from optparse import OptionParser
import sys
import time
from thomson_api import *

# Parsing argurments
parser = OptionParser()
parser.add_option("-j", "-J", dest="jobid", type="string",
                  help="Job ID/list Job ID", metavar=' ')

parser.add_option("-s", "-S", dest="state", type="string",
                  help="State/ Action (start, stop,...)", metavar=' ')

(options, args) = parser.parse_args()

#Check argurments
for option in ('jobid', 'state'):
    if not getattr(options, option):
        print 'Option %s not specified' % option
        parser.print_help()
        sys.exit(0)

print options.jobid
print options.state
print JobDetail(options.jobid).send_action(options.state)
