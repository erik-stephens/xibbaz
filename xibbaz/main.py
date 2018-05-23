"""
A wrapper around scripts to facilitate a single Dockerfile ENTRYPOINT.

  usage: xibbaz.main <cmd> ...

Where <cmd> is one of the following.  Use `-h, --help` for cmd specific usage.
  - cli
  - group
  - template
  - triggers
"""

import sys
import importlib

if len(sys.argv) >= 2:
    if sys.argv[1] not in ('cli', 'group', 'template', 'triggers'):
        print(__doc__)
    else:
        importlib.import_module('xibbaz.cmd.' + sys.argv[1]).main(sys.argv[2:])
else:
    print(__doc__)
