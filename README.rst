xibbaz: backwards zabbix
========================

Home page: https://github.com/erik-stephens/xibbaz
 
.. image:: https://img.shields.io/pypi/v/xibbaz.svg
    :target: https://pypi.python.org/pypi/xibbaz

.. image:: https://api.travis-ci.org/erik-stephens/xibbaz.png?branch=master,develop
   :target: http://travis-ci.org/erik-stephens/xibbaz
 

Goals
-----

- Be self-documenting.  Should not have to flip between the Zabbix API
  docs and a python REPL.

- Be discoverable.  Should not have to be familiar with the Zabbix API
  to get started.  Relationships between Zabbix objects should be easy
  and natural to discover.  Want to avoid being a thin wrapper around
  the JSON api like this::

    params = dict(...)
    group = api.response('hostgroup.get', params)
    hosts = api.response('host.get', groupids=group['result'][0]['groupid'])

  in favor of something like this::

    group = api.group('Maintenance')
    host = api.host('needs-work.com')
    group.add_hosts(host)
    for host in group.hosts.values():
        print('{} is in maintenance'.format(host))

- Be notebook friendly. Zabbix is great at collecting data and triggering
  alerts, but makes it difficult to navigate the data. Coupled with the likes of
  IPython Notebook & Pandas, it should be easy to analyze and visualize the
  data. Notebooks can be shared, serve as dashboards, generate reports, etc.

- Minimize server load and improve latency with aggressive caching of objects.

- Be idiomatic (mostly about packaging). This was initially a non-goal but it's
  better to spend a little bit of effort to be a good citizen. If this becomes a
  drag, then will become a non-goal.


Non-Goals
---------

- Minimal lines of code. There is a lot of boiler-plate and copy-pasta from
  zabbix documentation. That is ok. For the fewest lines of code, please refer
  to curl, wget, httpie, et al.

- Completeness. The implemented portions of the zabbix api reflect the need to
  satisfy known use cases in the real world.

- DRY-ness (Don't Repeat Yourself). There are plenty of opportunities to factor
  out common bits.


How to REPL
-----------

An example of how to bootstrap in interactive session::

    $ cat ixibbaz.py
    import xibbaz
    import keyring
    import os
    api = xibbaz.Api('https://zabbix.yours')
    username = os.environ.get('ZABBIX_USER', os.environ.get('USER'))
    api.login(username, keyring.get_password('zabbix-api', username))
    api.groups?
    from xibbaz import objects
    objects.Group?

    $ python3 -m IPython -i ixibbaz.py

Scripts
-------

  Authentication
  --------------
  Environment variables are used for your zabbix api credentials:

  - ZABBIX_API: the base url for your zabbix server's api
  - ZABBIX_USER: defaults to `USER` from environment
  - ZABBIX_PASS: defaults to using keyring('zabbix-api', ZABBIX_USER)

  group
  -----

  Add hosts to a group::

    ZABBIX_API=https://zabbix PYTHONPATH=.:.pip python3 -m xibbaz.main group add 'On-Demand Maintenance' needs-some-work.com

  cli
  ---
  There is a `cli` script to help support one-liners & simple shell scripts.
  Contrary to the "dont' be a thin api wrapper" goal, this script is basically
  that with some integrated `jq` support for systems without good json support.

  There are two flavors of the docker image, with or without `--jq` support which
  requires build dependencies.

  Some examples:

  - Look up a group and its linked hosts by name::

    ZABBIX_API=https://zabbix PYTHONPATH=.:.pip python3 -m xibbaz.main cli group get filter:name:'On-Demand Maintenance'
    [
      {
        "groupid": "42",
        "name": "On-Demand Maintenance",
        "internal": 0,
        "flags": 0,
        "hosts": [
          {...}
        ]
      }
    ]

  - Enumerate hosts in a group::

    make build
    docker run --env-file .env --rm xibbaz:jq cli --jq 'first | .hosts | map({hostid, name})' group get filter:name:'On-Demand Maintenance'
    [
      {
        "hostid": "11878",
        "name": "needs-some-work.com"
      }
    ]

  triggers
  --------

  Reports trigger status for a host (see `--help` for details). Example::

    ZABBIX_API=https://zabbix PYTHONPATH=.:.pip python3 -m xibbaz.main triggers -v -p warn some-host
    problem   high      some-host     Zabbix agent on some-host is unreachable for 5 minutes
    ok        average   some-host     some-host is unavailable by ICMP
    ok        average   some-host     SSH service is down on some-host


TODO
----

- ACK's for a trigger so an operator can quickly see history & remediations.
- Noisy triggers
- Noisy hosts


About the Name
--------------

- Disambiguation from other python zabbix projects.
- This was the only cool name left.
- An homage to our favorite zabbix forum user.
- Zabbix makes heads hurt and eyes bleed. Backwards might be more intuitive.
