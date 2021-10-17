#! /usr/bin/env python

"""
create a directory in the FileCatalog

Examples:
  $ dmkdir ./some_lfn_dir
"""

import os

import DIRAC
from COMDIRAC.Interfaces import ConfigCache
from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

from COMDIRAC.Interfaces import critical
from COMDIRAC.Interfaces import DSession
from COMDIRAC.Interfaces import createCatalog
from COMDIRAC.Interfaces import pathFromArguments

if __name__ == "__main__":

    from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

    configCache = ConfigCache()
    Script.registerArgument(["Path:     path to new directory"])
    Script.parseCommandLine(ignoreErrors=True)
    configCache.cacheConfig()

    args = Script.getPositionalArgs()

    session = DSession()

    catalog = createCatalog()

    result = catalog.createDirectory(pathFromArguments(session, args))
    if result["OK"]:
        if result["Value"]["Failed"]:
            for p in result["Value"]["Failed"]:
                print('ERROR - "%s": %s' % (p, result["Value"]["Failed"][p]))
    else:
        print("ERROR: %s" % result["Message"])
