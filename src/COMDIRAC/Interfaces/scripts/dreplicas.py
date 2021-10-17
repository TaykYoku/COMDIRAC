#! /usr/bin/env python

"""
list replicas for files in the FileCatalog
"""

import DIRAC
from COMDIRAC.Interfaces import critical, error
from COMDIRAC.Interfaces import DSession
from COMDIRAC.Interfaces import DCatalog
from COMDIRAC.Interfaces import pathFromArgument
from DIRAC.Core.Utilities.ReturnValues import returnSingleResult

if __name__ == "__main__":
    from COMDIRAC.Interfaces import ConfigCache
    from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

    configCache = ConfigCache()
    Script.registerArgument(["lfn:     logical file name"])
    Script.parseCommandLine(ignoreErrors=True)
    configCache.cacheConfig()

    args = Script.getPositionalArgs()

    session = DSession()
    catalog = DCatalog()

    exitCode = 0

    for arg in args:
        # lfn
        lfn = pathFromArgument(session, args[0])
        # fccli.do_replicas( lfn )
        ret = returnSingleResult(catalog.catalog.getReplicas(lfn))
        if ret["OK"]:
            replicas = ret["Value"]
            print(lfn + ":")
            for se, path in replicas.items():
                print("  ", se, path)
        else:
            error(lfn + ": " + ret["Message"])
            exitCode = -2

DIRAC.exit(exitCode)
