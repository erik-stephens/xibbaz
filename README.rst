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

    group = api.host_group('Maintenance')
    host = api.host('needs-work.com')
    group.add_hosts(host)
    for host in group.hosts.values():
        print('{} is in maintenance'.format(host))

- Support ad hoc analysis.  Zabbix is great at collecting data and
  triggering alerts, but makes it difficult to navigate the data.
  Coupled with the likes of IPython Notebook & Pandas, it should be
  easy to analyze and visual the data.  Even better, notebooks can be
  saved and shared as a kind of dashboard or report, which can be
  re-evaluated as needed or captured as a snapshot to PDF.

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


TODO
----

- Template [un]linking on service install & remove.
- ACK's for a trigger so an operator can quickly see history & remediations.
- Current active trigger list.
- Noisy triggers
- Current active triggered host list.
- Noisy hosts


About the Name
--------------

- Disambiguation from other python zabbix projects.
- This was the only cool name left.
- An homage to our favorite zabbix forum user.
- Zabbix makes heads hurt and eyes bleed. Backwards might be more intuitive.
