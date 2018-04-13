"""
Report trigger status for a host.  Number of problems is exit code.

Usage: COMMAND [options] [<host>]

Arguments:
  - host: zabbix hostname to report problems for (defaults to `hostname`)

Options:
  -v, --verbose
    Report status of all checks, not just current problems
  -p, --min-priority LEVEL
    Report these triggers only: all, info, warn, avg, high, disaster [default: info]
  --api URL
    Zabbix API endpoint (defaults to ZABBIX_API from environment)
"""
import os
import socket
import sys
from docopt import docopt
from . import Api, objects


def main(argv):
    opts = docopt(__doc__, argv)
    hostname = opts.get('<host>') or socket.gethostname()
    verbose = opts.get('--verbose')
    min_priority = dict(
        all = 0,
        info = 1,
        warn = 2,
        avg = 3,
        high = 4,
        disaster = 5,
    ).get(opts['--min-priority'])
    if min_priority is None:
        print('invalid --min-priority', file=sys.stderr)
        sys.exit(1)

    api = Api(opts.get('--api') or os.environ['ZABBIX_API'])
    if 'ZABBIX_USER' in os.environ:
        username = os.environ['ZABBIX_USER']
    else:
        username = os.environ['USER']
    if 'ZABBIX_PASS' in os.environ:
        password = os.environ['ZABBIX_PASS']
    else:
        import keyring
        password = keyring.get_password('zabbix-api', username)
    api.login(username, password)

    host = api.host(hostname)
    status = 0
    for t in sorted(host.triggers, key = lambda i: (i.value.val, i.priority.val), reverse=True):
        if t.priority.val >= min_priority:
            problematic = t.value.val > 0
            if problematic:
                status += 1
            if verbose or problematic:
                print("{:8}  {:12}  {}".format(t.value, t.priority, t.description))
    sys.exit(status)


if __name__ == '__main__':
    main(sys.argv)
