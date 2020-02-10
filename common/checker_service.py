from common.helpers.ssh_check import ssh_check
from common.helpers.snmp_check import snmpget
from common.helpers.ping_check import ping_check
from common.helpers.logger import log
from config import CHECKED_HOSTS


def check(client, *args):
    USERNAME, SNMPv3_SECRET, SSH_SECRET, COMMUNITY = args

    # check PING status
    res_ping = ping_check(client)

    # check SSH status
    res_ssh = ssh_check(hostname=client, username=USERNAME, password=SSH_SECRET)

    # check SNMP status
    res_snmpv2c = not not snmpget(client, '.1.3.6.1.2.1.1.1.0', community=COMMUNITY)
    res_snmpv3 = not not snmpget(client, '.1.3.6.1.2.1.1.1.0', version='3',
                                 user=USERNAME, authkey=SNMPv3_SECRET, privkey=SNMPv3_SECRET)

    # logs checked hosts
    if (type(res_ping) is float) and res_ssh and (res_snmpv2c or res_snmpv3):
        log(CHECKED_HOSTS, client, logtime=False)

    return res_ping, res_ssh, res_snmpv2c, res_snmpv3
