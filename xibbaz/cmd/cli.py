"""
Thin CLI wrapper around zabbix api.

Usage: COMMAND [options] <entity> <method> <params>...

Arguments:
  - entity: the kind of object to query (host, group, template)
  - method: the api call/method/verb (eg get, update, massadd) - not all supported
  - params: the arguments to pass to entity's `get` api call.

Options:
  -d, --debug
    Show debug output.
  --jq SCRIPT
    Use embedded jq library to process results.
  --api URL
    Zabbix API endpoint (defaults to ZABBIX_API from environment)

Refer to zabbix api documentation for details:
  - https://www.zabbix.com/documentation/3.4/manual/api
"""
from . import *
import json


def main(argv):
    opts = docopt(__doc__, argv)
    entity = opts['<entity>']
    params = dict(i.split(':', 1) for i in opts['<params>'])
    debug = opts['--debug']

    jq = None
    if opts['--jq']:
        try:
            import pyjq
        except ImportError:
            print('pyjq package required for jq script support', file=sys.stderr)
            sys.exit(1)
        jq = pyjq.compile(opts['--jq'])

    api = login(opts.get('--api'))

    if 'filter' in params:
        params['filter'] = dict(i.split(':', 1) for i in params['filter'].split('+'))
        for name, val in params['filter'].items():
            params['filter'][name] = val.split(',')
    if 'search' in params:
        params['search'] = dict(i.split(':', 1) for i in params['search'].split('+'))
        for name, val in params['search'].items():
            params['search'][name] = val.split(',')
    for name, val in params.items():
        if isinstance(val, str) and val.lower() in ['true', 'True', 'yes', 'Yes']:
            params[name] = True
    if 'limit' not in params:
        params['limit'] = 10
    if 'searchByAny' not in params:
        params['searchByAny'] = False
    if 'startSearch' not in params:
        params['startSearch'] = True
    if debug:
        print('DEBUG params:')
        json.dump(params, sys.stdout, indent=2)
        print('')

    Entity = getattr(objects, entity, None)
    if not Entity:
        print('unknown entity:', entity, file=sys.stderr)
        sys.exit(1)
    method = getattr(Entity, opts['<method>'], None)
    if not method:
        print('unsupported method:', opts['<method>'], file=sys.stderr)
        sys.exit(1)
    result = method(api, **params)
    if jq:
        result = jq.first([i.json() for i in result])
    json.dump(result, sys.stdout, indent=2, default=lambda i: i.json())


if __name__ == '__main__':
    main(sys.argv[1:])
