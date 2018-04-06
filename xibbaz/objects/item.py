
from datetime import datetime
from .api import ApiObject


class Item(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/item/object
    """

    # See `value_type` property
    TYPE_FLOAT = 0
    TYPE_CHAR  = 1
    TYPE_LOG   = 2
    TYPE_INT   = 3
    TYPE_TEXT  = 4

    def hosts(self):
        """
        List of `Hosts` with this item.
        """
        # Import here to avoid circular imports.
        from .host import Host
        return [Host(self._api, **host) for host in
                self._api.response('host.get', itemids=self.id).get('result')]


    def get_history(self, ts_from=None, ts_to=None, limit=10):
        """
        Return latest `limit` (ts, val) pairs from `ts_from` until `ts_to`.
        """
        params = dict(
            output = 'extend',
            history = self.value_type.val,
            itemids = self.id,
            limit = limit,
            sortfield = 'clock',
            sortorder = 'DESC',
        )
        if ts_from:
            params['time_from'] = ts_from.strftime('%s')
        if ts_to:
            params['time_till'] = ts_to.strftime('%s')
        return [(i['clock'], self._typed_value(i['value'])) for i in
                self._api.response('history.get', **params).get('result')]


    def __repr__(self):
        return "{}[{}]".format(self.__class__.__name__, self.key_.val)


    def _typed_value(self, val):
        """
        Return `val` with proper type based on this Item's `value_type`.
        """
        if self.value_type.val == self.TYPE_FLOAT:
            val = float(val)
        elif self.value_type.val == self.TYPE_INT:
            val = int(val)
        return val


    PROPS = dict(
        itemid = dict(
            doc = "ID of the item.",
            id = True,
            kind = int,
            readonly = True,
        ),
        delay = dict(
            doc = "Update interval of the item in ${val}${units} form.  Units: s=seconds (default), m=minutes, h=hours, d=days.",
            kind = str,
        ),
        hostid = dict(
            doc = "ID of the host that the item belongs to.",
        ),
        interfaceid = dict(
            doc = "ID of the item's host interface. Used only for host items. Optional for Zabbix agent (active), Zabbix internal, Zabbix trapper, Zabbix aggregate, database monitor and calculated items.",
        ),
        key_ = dict(
            doc = "Item key.",
        ),
        name = dict(
            doc = "Name of the item.",
        ),
        type = dict(
            doc = " Type of the item.",
            kind = int,
            vals = {
                0: 'Zabbix agent',
                1: 'SNMPv1 agent',
                2: 'Zabbix trapper',
                3: 'simple check',
                4: 'SNMPv2 agent',
                5: 'Zabbix internal',
                6: 'SNMPv3 agent',
                7: 'Zabbix agent (active)',
                8: 'Zabbix aggregate',
                9: 'web item',
                10: 'external check',
                11: 'database monitor',
                12: 'IPMI agent',
                13: 'SSH agent',
                14: 'TELNET agent',
                15: 'calculated',
                16: 'JMX agent',
                17: 'SNMP trap',
            },
        ),
        value_type = dict(
            doc = "Type of information of the item.",
            kind = int,
            vals = {
                0: 'numeric float',
                1: 'character',
                2: 'log',
                3: 'numeric unsigned',
                4: 'text',
            },
        ),
        authtype = dict(
            doc = "SSH authentication method. Used only by SSH agent items.",
            kind = int,
            vals = {
                0: 'password (default)',
                1: 'public kek',
            },
        ),
        data_type = dict(
            doc = "Data type of the item.",
            kind = int,
            vals = {
                0: 'decimal (default)',
                1: 'octal',
                2: 'hexadecimal',
                3: 'boolean',
            },
        ),
        delay_flex = dict(
            doc = "Flexible intervals as a serialized string.  Each serialized flexible interval consists of an update interval and a time period separated by a forward slash. Multiple intervals are separated by a colon.",
        ),
        delta = dict(
            doc = "Value that will be stored.",
            kind = int,
            vals = {
                0: 'as is (default)',
                1: 'Delta, speed per second',
                2: 'Delta, simple change',
            },
        ),
        description = dict(
            doc = "Description of the item.",
        ),
        error = dict(
            doc = "Error text if there are problems updating the item.",
            readonly = True,
        ),
        flags = dict(
            doc = "Origin of the item.",
            kind = int,
            readonly = True,
            vals = {
                0: 'a plain item',
                4: 'a discovered item',
            },
        ),
        # formula	 = dict(
        #     doc = "Custom multiplier.",
        #     kind = int,
        # ),
        history	 = dict(
            doc = "Retention of raw samples in ${val}${units} form.  Units: s=seconds (default), m=minutes, h=hours, d=days.",
            kind = str,
        ),
        inventory_link = dict(
            doc = "ID of the host inventory field that is populated by the item.  Refer to the host inventory page for a list of supported host inventory fields and their IDs.",
            kind = int,
        ),
        ipmi_sensor = dict(
            doc = "IPMI sensor. Used only by IPMI items.",
        ),
        lastclock = dict(
            doc = "Time when the item was last updated.",
            kind = datetime,
            readonly = True,
        ),
        lastns = dict(
            doc = "Nanoseconds when the item was last updated.",
            kind = int,
            readonly = True,
        ),
        lastvalue = dict(
            doc = "Last value of the item.",
            readonly = True,
        ),
        logtimefmt = dict(
            doc = "Format of the time in log entries. Used only by log items.",
        ),
        mtime = dict(
            doc = "Time when the monitored log file was last updated. Used only by log items.",
            kind = datetime,
        ),
        multiplier = dict(
            doc = "Whether to use a custom multiplier.",
            kind = int,
        ),
        params = dict(
            doc = "Additional parameters depending on the type of the item: - executed script for SSH and Telnet items; - SQL query for database monitor items; - formula for calculated items.",
        ),
        password = dict(
            doc = "Password for authentication. Used by simple check, SSH, Telnet, database monitor and JMX items.",
        ),
        port = dict(
            doc = "Port monitored by the item. Used only by SNMP items.",
        ),
        prevvalue = dict(
            doc = "Previous value of the item.",
            readonly = True,
        ),
        privatekey = dict(
            doc = "Name of the private key file.",
        ),
        publickey = dict(
            doc = "Name of the public key file.",
        ),
        snmp_community = dict(
            doc = "SNMP community. Used only by SNMPv1 and SNMPv2 items.",
        ),
        snmp_oid = dict(
            doc = "SNMP OID.",
        ),
        snmpv3_authpassphrase = dict(
            doc = "SNMPv3 auth passphrase. Used only by SNMPv3 items.",
        ),
        snmpv3_authprotocol = dict(
            doc = "SNMPv3 authentication protocol. Used only by SNMPv3 items.",
            kind = int,
            vals = {
                0: 'MD5 (default)',
                1: 'SHA',
            },
        ),
        snmpv3_contextname = dict(
            doc = "SNMPv3 context name. Used only by SNMPv3 items.",
        ),
        snmpv3_privpassphrase = dict(
            doc = "SNMPv3 priv passphrase. Used only by SNMPv3 items.",
        ),
        snmpv3_privprotocol = dict(
            doc = "SNMPv3 privacy protocol. Used only by SNMPv3 items.",
            kind = int,
            vals = {
                0: 'DES (default)',
                1: 'AES',
            },
        ),
        snmpv3_securitylevel = dict(
            doc = "SNMPv3 security level. Used only by SNMPv3 items.",
            kind = int,
            vals = {
                0: 'noAuthNoPriv',
                1: 'authNoPriv',
                2: 'authPriv',
            },
        ),
        snmpv3_securityname = dict(
            doc = "SNMPv3 security name. Used only by SNMPv3 items.",
        ),
        state = dict(
            doc = "State of the item.",
            kind = int,
            readonly = True,
            vals = {
                0: 'normal (default)',
                1: 'not supported',
            },
        ),
        status = dict(
            doc = "Status of the item.",
            kind = int,
            vals = {
                0: 'enabled item (default)',
                1: 'disabled item',
            },
        ),
        templateid = dict(
            doc = "ID of the parent template item.",
            readonly = True,
        ),
        trapper_hosts = dict(
            doc = "Allowed hosts. Used only by trapper items.",
        ),
        trends = dict(
            doc = "Retention of down-sampled data in ${val}${units} form.  Units: s=seconds (default), m=minutes, h=hours, d=days.",
            kind = str,
        ),
        units = dict(
            doc = "Value units.",
        ),
        username = dict(
            doc = "Username for authentication. Used by simple check, SSH, Telnet, database monitor and JMX items. Required by SSH and Telnet items.",
        ),
        valuemapid = dict(
            doc = "ID of the associated value map.",
        ),
    )
