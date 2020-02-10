import argparse
from ipaddress import ip_address
import os
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from waitress import serve

from common.checker_service import check
from config import *
from common.helpers.logger import log

# defaults or ENVs
USERNAME = os.getenv('NPM_RESOLVER_API_USERNAME', defaults['USERNAME'])
SNMPv3_SECRET = os.getenv('NPM_RESOLVER_API_SNMPv3_SECRET', defaults['SNMPv3_SECRET'])
SSH_SECRET = os.getenv('NPM_RESOLVER_API_SSH_SECRET', defaults['SSH_SECRET'])
COMMUNITY = os.getenv('NPM_RESOLVER_API_COMMUNITY', defaults['COMMUNITY'])
PORT = os.getenv('NPM_RESOLVER_API_PORT', defaults['PORT'])

app = Flask(__name__)
CORS(app)
api = Api(app)


class _Api(Resource):
    def get(self):
        log(RUNTIMELOG, '[{}]: {} {}'.format(request.remote_addr, request.method, request.url), output=True)
        return {'version': defaults['VERSION']}


class Checker(Resource):
    def get(self):
        log(RUNTIMELOG, '[{}]: {} {}'.format(request.remote_addr, request.method, request.url), output=True)
        ip = request.args['ip']

        try:
            ip_address(ip)
        except:
            return {'error': 'not valid IP address'}, 400

        # --- MOCK server
        # from time import sleep
        # if ip == '1.1.1.1':
        #     sleep(1)
        #     return {
        #         'ip': ip,
        #         'icmp': 1.12345,
        #         'ssh': True,
        #         'snmpv2c': True,
        #         'snmpv3': True
        #     }
        # elif ip == '1.1.1.2':
        #     sleep(1)
        #     return {
        #         'ip': ip,
        #         'icmp': False,
        #         'ssh': False,
        #         'snmpv2c': False,
        #         'snmpv3': False
        #     }
        # ------------------------

        res_ping, res_ssh, res_snmpv2, res_snmpv3 = check(ip, USERNAME, SNMPv3_SECRET, SSH_SECRET, COMMUNITY)

        return {
            'ip': ip,
            'icmp': res_ping,
            'ssh': res_ssh,
            'snmpv2c': res_snmpv2,
            'snmpv3': res_snmpv3
        }


api.add_resource(_Api, '/api/version')
api.add_resource(Checker, '/api/check')


def init():
    parser = argparse.ArgumentParser(description='NPM responder API server')

    parser.add_argument('--port', '-p', dest='port', type=int,
                        help='port for listening (5001 by default)')
    parser.add_argument('--user', '-u', dest='username', type=str,
                        required=True if not USERNAME else False,
                        help='username for SSH and SNMPv3 connections')
    parser.add_argument('--snmpv3-secret', dest='snmpv3_secret', type=str,
                        required=True if not SNMPv3_SECRET else False,
                        help='secret for SNMPv3 connections')
    parser.add_argument('--ssh-secret', dest='ssh_secret', type=str,
                        required=True if not SSH_SECRET else False,
                        help='secret for SSH connections')
    parser.add_argument('--community', '-c', dest='community', type=str,
                        help='community for SNMPv2 connections (\'public\' by default')
    parser.add_argument('--version', '-v', action='version', version='NPM responder API server v{}'.format(defaults['VERSION']),
                        help='show app version')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # get params
    args = init()

    # override default settings
    USERNAME = args.username if args.username else USERNAME
    SNMPv3_SECRET = args.snmpv3_secret if args.snmpv3_secret else SNMPv3_SECRET
    SSH_SECRET = args.ssh_secret if args.ssh_secret else SSH_SECRET
    COMMUNITY = args.community if args.community else COMMUNITY
    PORT = args.port if args.port else PORT

    # Create ./logs dir if it doesn't exist
    if not os.path.exists(defaults['LOGDIR']):
        os.mkdir(defaults['LOGDIR'])

    # start development version
    # app.run(port=PORT, debug=False)

    # start production version on waitress
    serve(app, host='0.0.0.0', port=PORT)