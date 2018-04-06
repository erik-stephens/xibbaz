"""
Thin CLI wrapper around zabbix api.

Usage: COMMAND [options] <entity> <method> <params>...

Arguments:
  - entity: the kind of object to query (host, hostgroup, template)
  - method: the api call/method/verb (eg get, update, massadd) - not all supported
  - params: the arguments to pass to entity's `get` api call.

Options:
  -v, --verbosity LEVEL
    trace, debug, info, warn, error, fatal [default: warn]
  --jq SCRIPT
    Use embedded jq library to process results.
  --api URL
    Zabbix API endpoint (defaults to ZABBIX_API from environment)

Refer to zabbix api documentation for details:
  - https://www.zabbix.com/documentation/3.4/manual/api
"""

if __name__ == '__main__':
    from . import Api, objects
    import json
    import os
    import sys

    from docopt import docopt
    opts = docopt(__doc__)
    entity = opts['<entity>']
    params = dict(i.split(':', 1) for i in opts['<params>'])

    jq = None
    if opts['--jq']:
        try:
            import pyjq
        except ImportError:
            print('pyjq package required for jq script support', file=sys.stderr)
            sys.exit(1)
        jq = pyjq.compile(opts['--jq'])

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
    # print('params:', params)
    # sys.exit(1)
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
