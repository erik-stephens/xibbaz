"""
A stupid wrapper around scripts to facilitate a single Dockerfile ENTRYPOINT.
"""

import sys
import importlib

importlib.import_module('xibbaz.cmd.' + sys.argv[1]).main(sys.argv[2:])
