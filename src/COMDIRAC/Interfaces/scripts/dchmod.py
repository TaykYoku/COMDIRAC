#! /usr/bin/env python
########################################################################
# $HeadURL$
########################################################################

"""
Change file mode bits

Examples:
  $ dchmod 755 ././some_lfn_file
  $ dchmod -R 700 ./
"""

from COMDIRAC.Interfaces import ConfigCache
from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script
from DIRAC import S_OK


class Params:
    def __init__(self):
        self.recursive = False

    def setRecursive(self, opt):
        self.recursive = True
        return S_OK()

    def getRecursive(self):
        return self.recursive


params = Params()

Script.registerArgument("mode:     octal mode bits")
Script.registerArgument(["Path:     path to file"], mandatory=False)
Script.registerSwitch("R", "recursive", "recursive", params.setRecursive)

configCache = ConfigCache()
Script.parseCommandLine(ignoreErrors=True)
configCache.cacheConfig()

args = Script.getPositionalArgs()

import DIRAC
from DIRAC import gLogger
from COMDIRAC.Interfaces import DSession
from COMDIRAC.Interfaces import DCatalog
from COMDIRAC.Interfaces import pathFromArgument

session = DSession()
catalog = DCatalog()

mode = args[0]

lfns = []
for path in args[1:]:
    lfns.append(pathFromArgument(session, path))

from DIRAC.Resources.Catalog.FileCatalog import FileCatalog

fc = FileCatalog()

for lfn in lfns:
    try:
        pathDict = {lfn: eval("0" + mode)}
        result = fc.changePathMode(pathDict, params.recursive)
        if not result["OK"]:
            gLogger.error("Error:", result["Message"])
            break
        if lfn in result["Value"]["Failed"]:
            gLogger.error("Error:", result["Value"]["Failed"][lfn])
    except Exception as x:
        print("Exception:", str(x))
