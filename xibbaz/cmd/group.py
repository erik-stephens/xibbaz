#! /usr/bin/env python3
"""
Add or remove hosts to a group. Useful for putting hosts into & out of a
special group for on-demand maintenance.

Usage: COMMAND [options] <verb> <group> <hosts>...

Arguments:
  - verb: `add` or `remove`
  - group: name of zabbix group
  - hosts: one or more hostnames

Options:
  --api URL
    Zabbix API endpoint (defaults to ZABBIX_API from environment)
"""
from . import *


def main(argv):
    opts = docopt(__doc__, argv)
    verb = opts.get('<verb>')

    api = login(opts.get('--api'))
    group = api.group(opts.get('<group>'))
    hosts = map(api.host, opts.get('<hosts>'))
    if verb == 'remove':
        group.remove_hosts(*hosts)
    else:
        group.add_hosts(*hosts)


if __name__ == '__main__':
    main(sys.argv[1:])
