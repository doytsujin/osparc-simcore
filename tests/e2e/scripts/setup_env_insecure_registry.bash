#!/bin/bash
#
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

# prepare simcore .env
make .env
# disable email verification
echo WEBSERVER_LOGIN_REGISTRATION_INVITATION_REQUIRED=0 >>.env
echo WEBSERVER_LOGIN_REGISTRATION_CONFIRMATION_REQUIRED=0 >>.env

# set max number of CPUs sidecar
echo SERVICES_MAX_NANO_CPUS=2000000000 >> .env
# set up insecure internal registry
echo REGISTRY_AUTH=False >> .env
echo REGISTRY_SSL=False >> .env
echo REGISTRY_URL=registry:5000 >> .env
# disable registry caching to ensure services are fetched
echo DIRECTOR_REGISTRY_CACHING=False >> .env

# prepare insecure registry access for docker engine
# add host name to the insecure registry
sudo bash -c "echo '127.0.0.1 registry' >> /etc/hosts"
# add insecure registry into docker daemon and restart daemon
echo "------------------------ before modifying docker daemon"
sudo bash -c "echo '{\"insecure-registries\": [\"registry:5000\"]}' >> /etc/docker/daemon.json"
echo "------------------------ after modifying docker daemon"
sudo service docker restart
