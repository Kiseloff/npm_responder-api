# NPM responder api

#####API endpoints

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

##### Test Application

Python 3.7 is recommended

    mkdir npm_responer-api
    cd ./npm_responer-api/
    git clone https://github.com/Kiseloff/npm_responder-api.git .
    
    python3 -m venv env
    source env/bin/activate
    pip install --upgrade pip
    pip install -r ./requirements.txt
    
    python ./app.py [-p <PORT> -c <COMMUNITY> -v] -u <USERNAME> --snmpv3-secret <SNMPV3_SECRET> --ssh-secret <SSH_SECRET>

##### Build Docker image  

    git clone https://github.com/Kiseloff/npm_responder-api.git
    cd ./npm_responder-api
    docker build --no-cache --network=host -t npm_responder-api:<VERSION> .
    
    # push to hub.docker.com
    docker tag npm_responder-api:<VERSION> kiseloff/npm_responder-api:<VERSION>
    docker login
    docker push kiseloff/npm_responder-api:<VERSION>
    
##### Pull docker image

    docker pull kiseloff/npm_responder-api:latest
    
##### Show application version

    docker run -it --rm --name npm_responder-api-app kiseloff/npm_responder-api:<VERSION> -v

##### Run Docker container
    
    docker run -it -p <PORT>:<PORT> \
    -v ~/npm_responder_logs:/usr/src/app/logs \
    --name npm_responder-api-app kiseloff/npm_responder-api:<VERSION> \
    [-p <PORT> -c <COMMUNITY>] -u <USERNAME> --snmpv3-secret <SNMPV3_SECRET> --ssh-secret <SSH_SECRET>

##### Run Docker container as a daemon

    docker run -d -p <PORT>:<PORT> \
    -v ~/npm_responder_logs:/usr/src/app/logs \
    --name npm_responder-api-app kiseloff/npm_responder-api:<VERSION> \
    [-p <PORT> -c <COMMUNITY>] -u <USERNAME> --snmpv3-secret <SNMPV3_SECRET> --ssh-secret <SSH_SECRET>

    <PORT> - application listening port (default 8023)
    <COMMUNITY> - SNMPv2c RO community string (default 'public')
    <USERNAME> - SSH/SNMPv3 username
    <SNMPV3_SECRET> - SNMPv3 secret
    <SSH_SECRET> - SSH secret

##### Remove docker container and image

    docker rm -f npm_responder-api-app && docker rmi -f kiseloff/npm_responder-api:<VERSION>

##### CI/CD
    
[CI/CD Manual](https://www.digitalocean.com/community/tutorials/how-to-configure-a-continuous-integration-testing-environment-with-docker-and-docker-compose-on-ubuntu-14-04#step-3-%E2%80%94-create-the-%E2%80%9Chello-world%E2%80%9D-python-application)
    
    docker-compose -f ./docker-compose.test.yml -p ci build
    docker-compose -f ./docker-compose.test.yml -p ci up -d

    docker logs -f ci_sut_1
    docker wait ci_sut_1

##### Example

    docker run -d -p 8023:8023 \
    -v ~/npm_responder_logs:/usr/src/app/logs \
    --name npm_responder-api-app kiseloff/npm_responder-api:latest \
    -u SOME_USER --snmpv3-secret SOME_SNMP_PASS --ssh-secret SOME_SSH_PASS
