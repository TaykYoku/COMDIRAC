"""
  Retrieve logging information for a DIRAC job
"""

import DIRAC
from COMDIRAC.Interfaces import ConfigCache
from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script


class Params:
    def __init__(self):
        self.fmt = "pretty"

    def setFmt(self, arg=None):
        self.fmt = arg.lower()

    def getFmt(self):
        return self.fmt


params = Params()

Script.registerArgument(["JobID: a DIRAC job identifier"], mandatory=False)
Script.registerSwitch("f:", "Fmt=", "display format (pretty, csv, json)", params.setFmt)

configCache = ConfigCache()
Script.parseCommandLine(ignoreErrors=True)
configCache.cacheConfig()

args = Script.getPositionalArgs()

from DIRAC.Core.DISET.RPCClient import RPCClient
from COMDIRAC.Interfaces.Utilities.DCommands import ArrayFormatter

exitCode = 0

jobs = map(int, args)

monitoring = RPCClient("WorkloadManagement/JobMonitoring")
af = ArrayFormatter(params.getFmt())
headers = ["Status", "MinorStatus", "ApplicationStatus", "Time", "Source"]
errors = []
for job in jobs:
    result = monitoring.getJobLoggingInfo(job)
    if result["OK"]:
        print(af.listFormat(result["Value"], headers, sort=headers.index("Time")))
    else:
        errors.append(result["Message"])
        exitCode = 2

for error in errors:
    print("ERROR: %s" % error)

DIRAC.exit(exitCode)
