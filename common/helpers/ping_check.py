from ping3 import ping

from common.helpers.logger import log
from config import RUNTIMELOG


def ping_check(client):
    res_ping = ping(client, unit='ms')
    res_ping = res_ping if res_ping is not None else False
    log(RUNTIMELOG, '[ICMP to {}]: {}'
        .format(client, 'successfully' if (type(res_ping) is float) else 'timed out'), output=True)
    return res_ping
