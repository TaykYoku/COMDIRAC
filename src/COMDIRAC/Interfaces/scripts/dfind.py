#! /usr/bin/env python

"""
find files in the FileCatalog

Examples:
  $ dfind . "some_integer_metadata>1
"""

import DIRAC

from COMDIRAC.Interfaces import critical
from COMDIRAC.Interfaces import DSession
from COMDIRAC.Interfaces import DCatalog
from COMDIRAC.Interfaces import pathFromArgument

if __name__ == "__main__":

    from COMDIRAC.Interfaces import ConfigCache
    from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

    configCache = ConfigCache()
    Script.registerArgument("lfn:         directory entry in the FileCatalog")
    Script.registerArgument(['metaspec:    metadata index specifcation (of the form: "meta=value" or "meta<value", "meta!=value", etc.)'], mandatory=False)
    Script.parseCommandLine(ignoreErrors=True)
    configCache.cacheConfig()

    args = Script.getPositionalArgs()

    session = DSession()
    catalog = DCatalog()

    lfn = pathFromArgument(session, args[0])

    from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import (
        FileCatalogClientCLI,
    )

    fccli = FileCatalogClientCLI(catalog.catalog)

    fccli.do_find("-q " + lfn + " " + " ".join(args[1:]))
