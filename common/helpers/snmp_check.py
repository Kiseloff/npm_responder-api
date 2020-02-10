from pysnmp.hlapi import *

from common.helpers.logger import log
from config import RUNTIMELOG


def snmpprint(varBinds):
    for varBind in varBinds:  # SNMP response contents
        print(' = '.join([x.prettyPrint() for x in varBind]))


def snmpget(host, oid,
            community='public',
            version='2c',
            user='', authkey='', privkey='',
            authProtocol=usmHMACMD5AuthProtocol,
            privProtocol=usmAesCfb128Protocol,
            port=161):
    if version == '2c':
        iterator = getCmd(SnmpEngine(),
                          CommunityData(community),
                          UdpTransportTarget((host, port)),
                          ContextData(),
                          ObjectType(ObjectIdentity(oid))
                          )
    elif version == '3':
        iterator = getCmd(SnmpEngine(),
                          UsmUserData(user, authkey, privkey,
                                      authProtocol=authProtocol,
                                      privProtocol=privProtocol),
                          UdpTransportTarget((host, port)),
                          ContextData(),
                          ObjectType(ObjectIdentity(oid))
                          )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:  # SNMP engine errors
        log(RUNTIMELOG, '[SNMP{} to {}]: {}'.format('v2c' if version == '2c' else 'v3', host, errorIndication), output=True)
        return False
    else:
        if errorStatus:  # SNMP agent errors
            log(RUNTIMELOG, '[SNMP{} to {}]: {} at {}'.format('v2c' if version == '2c' else 'v3', host, errorStatus.prettyPrint(), varBinds[int(errorIndex) - 1] if errorIndex else '?'),
                output=True)
            return False
        else:
            log(RUNTIMELOG, '[SNMP{} to {}]: {}'.format('v2c' if version == '2c' else 'v3', host, 'successfully'), output=True)
            return True
