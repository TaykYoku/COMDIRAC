#! /usr/bin/env python

"""
register DCommands session environment variables
"""

from COMDIRAC.Interfaces import critical
from COMDIRAC.Interfaces import DSession

if __name__ == "__main__":
    from COMDIRAC.Interfaces import ConfigCache
    from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

    configCache = ConfigCache()
    Script.registerArgument(('section:              section (defaults to "session:environment")',
                             "section.option:       option name",
                             "section.option=value: set option value"), mandatory=False)
    Script.parseCommandLine(ignoreErrors=True)
    configCache.cacheConfig()

    args = Script.getPositionalArgs()

    session = DSession()

    modified = False
    for arg in args:
        section = None
        option = None

        arg, value = arg.split("=", 1)
        if "." in arg:
            section, option = arg.split(".", 1)
        else:
            option = arg

        if section:
            session.set(section, option, value)
        else:
            session.setEnv(option, value)
        modified = True

    if modified:
        session.write()
