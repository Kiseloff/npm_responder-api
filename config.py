defaults = {
    'USERNAME': '',
    'SNMPv3_SECRET': '',
    'SSH_SECRET': '',
    'COMMUNITY': 'public',
    'PORT': 5001,
    'CHECKED_HOSTS': 'checked_hosts.log',
    'RUNTIMELOG': 'api_runtime.log',
    'LOGDIR': './logs',
    'VERSION': '1.1.0',
}

RUNTIMELOG = '/'.join([defaults['LOGDIR'], defaults['RUNTIMELOG']])
CHECKED_HOSTS = '/'.join([defaults['LOGDIR'], defaults['CHECKED_HOSTS']])