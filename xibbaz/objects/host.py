
from datetime import datetime
from .api import ApiObject


class Host(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/host/object
    """

    DEFAULT_SELECTS = ('Groups', 'Applications', 'Macros', 'Graphs', 'Screens')

    RELATIONS = ('groups', 'templates', 'items', 'triggers', 'screens', 'graphs')


    @property
    def problems(self):
        """
        `[Problem]` of current problem Events.
        """
        return self._api.problems(hostids=self.id)


    PROPS = dict(
        hostid = dict(
            doc = "ID of the host.",
            id = True,
            readonly = True,
        ),
        host = dict(
            doc = "Technical name of the host.",
        ),
        available = dict(
            doc = "Availability of the agent.",
            kind = int,
            readonly = True,
            vals = {
                0: 'unknown (default)',
                1: 'available',
                2: 'unavailable',
            },
        ),
        disable_until = dict(
            doc = "The next polling time of an unavailable Zabbix agent.",
            kind = datetime,
            readonly = True,
        ),
        error = dict(
            doc = "Error text if Zabbix agent is unavailable.",
            readonly = True,
        ),
        errors_from = dict(
            doc = "Time when Zabbix agent became unavailable.",
            kind = datetime,
            readonly = True,
        ),
        flags = dict(
            doc = "Origin of the host.",
            kind = int,
            readonly = True,
            vals = {
                0: 'a plain host',
                4: 'a discovered host',
            },
        ),
        inventory_mode = dict(
            doc = "Host inventory population mode.",
            kind = int,
            vals = {
                -1: 'disabled',
                0 : 'manual (default)',
                1 : 'automatic',
            },
        ),
        ipmi_authtype = dict(
            doc = "IPMI authentication algorithm.",
            kind = int,
            vals = {
                -1: 'default (default)',
                0 : 'none',
                1 : 'MD2',
                2 : 'MD5',
                4 : 'straight',
                5 : 'OEM',
                6 : 'RMCP+',
            },
        ),
        ipmi_available = dict(
            doc = "Availability of IPMI agent.",
            kind = int,
            readonly = True,
            vals = {
                0: 'unknown (default)',
                1: 'available',
                2: 'unavailable',
            },
        ),
        ipmi_disable_until = dict(
            doc = "The next polling time of an unavailable IPMI agent.",
            kind = datetime,
            readonly = True,
        ),
        ipmi_error = dict(
            doc = "Error text if IPMI agent is unavailable.",
            readonly = True,
        ),
        ipmi_errors_from = dict(
            doc = "Time when IPMI agent became unavailable",
            kind = datetime,
            readonly = True,
        ),
        ipmi_password = dict(
            doc = "IPMI password",
        ),
        ipmi_privilege = dict(
            doc = "IPMI privilege level.",
            kind = int,
            vals = {
                1: 'callback',
                2: 'user (default)',
                3: 'operator',
                4: 'admin',
                5: 'OEM',
            },
        ),
        ipmi_username = dict(
            doc = "IPMI username",
        ),
        jmx_available = dict(
            doc = "Availability of JMX agent.",
            kind = int,
            readonly = True,
            vals = {
                0: 'unknown (default)',
                1: 'available',
                2: 'unavailable',
            },
        ),
        jmx_disable_until = dict(
            doc = "The next polling time of an unavailable JMX agent.",
            kind = datetime,
            readonly = True,
        ),
        jmx_error = dict(
            doc = "Error text if JMX agent is unavailable.",
            readonly = True,
        ),
        jmx_errors_from = dict(
            doc = "Time when JMX agent became unavailable.",
            kind = datetime,
            readonly = True,
        ),
        maintenance_from = dict(
            doc = "Starting time of the effective maintenance.",
            kind = datetime,
            readonly = True,
        ),
        maintenance_status = dict(
            doc = "Effective maintenance status.",
            kind = int,
            readonly = True,
            vals = {
                0: 'no maintenance (default)',
                1: 'maintenance in effect',
            },
        ),
        maintenance_type = dict(
            doc = "Effective maintenance type.",
            kind = int,
            readonly = True,
            vals = {
                0: 'maintenance with data collection (default)',
                1: 'maintenance without data collection',
            },
        ),
        maintenanceid = dict(
            doc = "ID of the `Maintenance` that is currently in effect on the host.",
            readonly = True,
        ),
        name = dict(
            doc = "Visible name of the host, defaults to `host` property value.",
        ),
        proxy_hostid = dict(
            doc = "ID of the `Proxy` that is used to monitor the host.",
        ),
        snmp_available = dict(
            doc = "Availability of SNMP agent.",
            kind = int,
            readonly = True,
            vals = {
                0: 'unknown (default)',
                1: 'available',
                2: 'unavailable',
            },
        ),
        snmp_disable_until = dict(
            doc = "The next polling time of an unavailable SNMP agent.",
            kind = datetime,
            readonly = True,
        ),
        snmp_error = dict(
            doc = "Error text if SNMP agent is unavailable.",
            readonly = True,
        ),
        snmp_errors_from = dict(
            doc = "Time when SNMP agent became unavailable.",
            kind = datetime,
            readonly = True,
        ),
        status = dict(
            doc = "Status and function of the host.",
            kind = int,
            vals = {
                0: 'monitored host (default)',
                1: 'unmonitored host',
            },
        ),
        tls_connect = dict(
            doc = "Connections to host.",
            kind = int,
            vals = {
                1: 'no encryption (default)',
                2: 'pre-shared key (PSK)',
                4: 'certificate',
            },
        ),
        tls_accept = dict(
            doc = "Connections from host.",
            kind = int,
            vals = {
                1: 'no encryption (default)',
                2: 'preshared key (PSK)',
                4: 'certificate',
            },
        ),
        tls_issuer = dict(
            doc = "Certificate issuer.",
        ),
        tls_subject = dict(
            doc = "Certificate subject.",
        ),
        tls_psk_identity = dict(
            doc = "PSK identity. Required if either tls_connect or tls_accept has PSK enabled.",
        ),
        tls_psk = dict(
            doc = "The preshared key, at least 32 hex digits. Required if either tls_connect or tls_accept has PSK enabled.",
        ),
    )
