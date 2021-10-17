#! /usr/bin/env python

"""
print DCommands session environment variables
"""

import DIRAC

from COMDIRAC.Interfaces import critical

from COMDIRAC.Interfaces import DSession

if __name__ == "__main__":
    from COMDIRAC.Interfaces import ConfigCache
    from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

    configCache = ConfigCache()
    Script.registerArgument(("section:        display all options in section",
                             "section.option: display section specific option"), mandatory=False)
    Script.parseCommandLine(ignoreErrors=True)
    configCache.cacheConfig()

    args = Script.getPositionalArgs()

    session = DSession()

    if not args:
        retVal = session.listEnv()
        if not retVal["OK"]:
            print("Error:", retVal["Message"])
            DIRAC.exit(-1)
        for o, v in retVal["Value"]:
            print(o + "=" + v)
        DIRAC.exit(0)

    arg = args[0]

    section = None
    option = None

    if "." in arg:
        section, option = arg.split(".")
    else:
        option = arg

    ret = None
    if section:
        ret = session.get(section, option)
    else:
        ret = session.getEnv(option)

    if not ret["OK"]:
        print(critical(ret["Message"]))

    print(ret["Value"])
