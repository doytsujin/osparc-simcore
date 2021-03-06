# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name

import subprocess
import time
from pathlib import Path
from pprint import pprint
from typing import Dict

import docker
import pytest
import tenacity
from servicelib.simcore_service_utils import SimcoreRetryPolicyUponInitialization
from .helpers.utils_docker import get_ip


@pytest.fixture(scope="session")
def docker_client() -> docker.client.DockerClient:
    client = docker.from_env()
    yield client


@pytest.fixture(scope="session")
def keep_docker_up(request) -> bool:
    return request.config.getoption("--keep-docker-up")


@pytest.fixture(scope="module")
def docker_swarm(
    docker_client: docker.client.DockerClient, keep_docker_up: bool
) -> None:
    try:
        docker_client.swarm.reload()
        print("CAUTION: Already part of a swarm")
        yield
    except docker.errors.APIError:
        docker_client.swarm.init(advertise_addr=get_ip())
        yield
        if not keep_docker_up:
            assert docker_client.swarm.leave(force=True)


@tenacity.retry(**SimcoreRetryPolicyUponInitialization().kwargs)
def _wait_for_services(docker_client: docker.client.DockerClient) -> None:
    pre_states = ["NEW", "PENDING", "ASSIGNED", "PREPARING", "STARTING"]
    services = docker_client.services.list()
    for service in services:
        print(f"Waiting for {service.name}...")
        if service.tasks():
            task = service.tasks()[0]
            if task["Status"]["State"].upper() not in pre_states:
                if not task["Status"]["State"].upper() == "RUNNING":
                    raise Exception(f"service {service.name} not running")


def _print_services(docker_client: docker.client.DockerClient, msg: str) -> None:
    print("{:*^100}".format("docker services running " + msg))
    for service in docker_client.services.list():
        pprint(service.attrs)
    print("-" * 100)


@pytest.fixture(scope="module")
def docker_stack(
    docker_swarm,
    docker_client: docker.client.DockerClient,
    core_services_config_file: Path,
    ops_services_config_file: Path,
    keep_docker_up: bool,
) -> Dict:
    stacks = {"simcore": core_services_config_file, "ops": ops_services_config_file}

    # make up-version
    stacks_up = []
    for stack_name, stack_config_file in stacks.items():
        subprocess.run(
            f"docker stack deploy -c {stack_config_file.name} {stack_name}",
            shell=True,
            check=True,
            cwd=stack_config_file.parent,
        )
        stacks_up.append(stack_name)

    _wait_for_services(docker_client)
    _print_services(docker_client, "[BEFORE TEST]")

    yield {
        "stacks": stacks_up,
        "services": [service.name for service in docker_client.services.list()],
    }

    _print_services(docker_client, "[AFTER TEST]")

    if keep_docker_up:
        # skip bringing the stack down
        return

    # clean up. Guarantees that all services are down before creating a new stack!
    #
    # WORKAROUND https://github.com/moby/moby/issues/30942#issue-207070098
    #
    #   docker stack rm services
    #   until [ -z "$(docker service ls --filter label=com.docker.stack.namespace=services -q)" ] || [ "$limit" -lt 0 ]; do
    #   sleep 1;
    #   done
    #   until [ -z "$(docker network ls --filter label=com.docker.stack.namespace=services -q)" ] || [ "$limit" -lt 0 ]; do
    #   sleep 1;
    #   done

    # make down
    # NOTE: remove them in reverse order since stacks share common networks
    WAIT_BEFORE_RETRY_SECS = 1
    stacks_up.reverse()
    for stack in stacks_up:
        subprocess.run(f"docker stack rm {stack}", shell=True, check=True)

        while docker_client.services.list(
            filters={"label": f"com.docker.stack.namespace={stack}"}
        ):
            time.sleep(WAIT_BEFORE_RETRY_SECS)

        while docker_client.networks.list(
            filters={"label": f"com.docker.stack.namespace={stack}"}
        ):
            time.sleep(WAIT_BEFORE_RETRY_SECS)

    _print_services(docker_client, "[AFTER REMOVED]")
