#! /usr/bin/env python

"""
Change current DIRAC File Catalog working directory

Examples:
  $ dcd /dirac/user
  $ dcd
"""

import os

from COMDIRAC.Interfaces import critical
from COMDIRAC.Interfaces import DSession
from COMDIRAC.Interfaces import DCatalog
from COMDIRAC.Interfaces import pathFromArgument
from COMDIRAC.Interfaces import ConfigCache

from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

configCache = ConfigCache()
Script.registerArgument(
    "Path: path to new working directory (defaults to home directory)", mandatory=False
)
Script.parseCommandLine(ignoreErrors=True)
configCache.cacheConfig()

args = Script.getPositionalArgs()

import DIRAC

session = DSession()

if len(args) > 1:
    print("Error: too many arguments provided\n%s:" % Script.scriptName)
    Script.showHelp()
    DIRAC.exit(-1)

if len(args):
    arg = pathFromArgument(session, args[0])
else:
    arg = session.homeDir()


catalog = DCatalog()

if catalog.isDir(arg):
    if session.getCwd() != arg:
        session.setCwd(arg)
        session.write()
else:
    critical('Error: "%s" not a valid directory' % arg)
