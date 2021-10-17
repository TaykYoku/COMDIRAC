#! /usr/bin/env python

"""
print DCommands working directory
"""

if __name__ == "__main__":
    from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script
    from COMDIRAC.Interfaces import DSession
    from COMDIRAC.Interfaces import ConfigCache

    configCache = ConfigCache()
    Script.parseCommandLine(ignoreErrors=True)
    configCache.cacheConfig()

    print(DSession().getCwd())
