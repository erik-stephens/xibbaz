#! /usr/bin/env python3
"""
Report trigger status.  Number of problems is exit code.

Usage: COMMAND [options] [<host>]

Arguments:
  - host: zabbix hostname to report problems for.  All hosts by default.

Options:
  -v, --verbose
    Report status of all checks, not just current problems, but only when a
    host is given.
  -p, --min-priority LEVEL
    Report these triggers only: all, info, warn, avg, high, disaster [default: info]
  --api URL
    Zabbix API endpoint (defaults to ZABBIX_API from environment)
"""
from . import *


def description(trigger):
    """
    Substitute some important macros, namely `{HOST.NAME}`.
    """
    s = trigger.description.val
    if trigger.hosts:
        s = s.replace('{HOST.NAME}', ', '.join(i.text for i in trigger.hosts))
    return s


def main(argv):
    opts = docopt(__doc__, argv)
    hostname = opts.get('<host>')
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

    api = login(opts.get('--api'))
    params = dict()
    if hostname:
        host = api.host(hostname)
        params['hostids'] = [host.id]
    else:
        params['only_true'] = 1
        params['active'] = 1
        params['monitored'] = 1
    status = 0
    for t in sorted(api.triggers(**params), key = lambda i: (i.value.val, i.priority.val), reverse=True):
        if t.priority.val >= min_priority:
            problematic = t.value.val > 0
            if problematic:
                status += 1
            if verbose or problematic:
                print("{:8}  {:12}  {:25}  {}".format(t.value, t.priority, t.hosts[0], description(t)))
    sys.exit(status)


if __name__ == '__main__':
    main(sys.argv[1:])
