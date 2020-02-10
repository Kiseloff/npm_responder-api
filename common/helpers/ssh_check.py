import socket
from time import sleep
import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException

from common.helpers.logger import log
from config import RUNTIMELOG


def ssh_check(hostname, username, password, timeout=2, initial_wait=0, interval=0, retries=2):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    sleep(initial_wait)

    for x in range(retries):
        try:
            client.connect(hostname=hostname, username=username, password=password, timeout=timeout)
            client.close()
            log(RUNTIMELOG, '[SSH to {}]: {}'.format(hostname, 'successfully'), output=True)
            return True
        except (BadHostKeyException,
                AuthenticationException,
                SSHException,
                socket.error) as e:
            log(RUNTIMELOG, '[SSH to {}]: {}'.format(hostname, e), output=True)
            sleep(interval)

    return False
