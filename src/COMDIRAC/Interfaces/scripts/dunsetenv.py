#! /usr/bin/env python

"""
remove DCommands session environment variables
"""

from COMDIRAC.Interfaces import critical

from COMDIRAC.Interfaces import DSession

if __name__ == "__main__":
    from COMDIRAC.Interfaces import ConfigCache
    from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

    configCache = ConfigCache()
    Script.registerArgument(("section:              display all options in section",
                             "section.option:       display section specific option"), mandatory=False)
    Script.parseCommandLine(ignoreErrors=True)
    configCache.cacheConfig()

    args = Script.getPositionalArgs()

    session = DSession()

    modified = False
    for arg in args:
        section = None
        option = None

        if "." in arg:
            section, option = arg.split(".")
        else:
            option = arg

        if section:
            session.remove(section, option)
        else:
            session.unsetEnv(option)

        modified = True

    if modified:
        session.write()
