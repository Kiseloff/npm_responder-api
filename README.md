#####API requests

    GET http://127.0.0.1:5000/api/version
    {
        'version': 'x.x.x'
    }
    
    GET http://127.0.0.1:5000/api/check?ip=X.X.X.X
    {
        'status': 'OK',
        'proto': {
            'icmp': '',
            'ssh': '',
            'snmpv2c': '',
            'snmpv3': ''
        }
    }