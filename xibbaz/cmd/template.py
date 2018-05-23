#! /usr/bin/env python3
"""
Add or remove hosts to a template.

Usage: COMMAND [options] <verb> <template> <hosts>...

Arguments:
  - verb: `add` or `remove`
  - template: name of zabbix template
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
    template = api.template(opts.get('<template>'))
    hosts = map(api.host, opts.get('<hosts>'))
    if verb == 'remove':
        template.remove_hosts(*hosts)
    else:
        template.add_hosts(*hosts)


if __name__ == '__main__':
    main(sys.argv[1:])
