import logging
from typing import List

import click

from .config import RABBIT_CONFIG
from .core import inspect
from .db import DBContextManager
from .rabbitmq import RabbitMQ
from .utils import wrap_async_call

log = logging.getLogger(__name__)


@click.command()
@click.option("--job_id", default=0, type=int, help="The job ID")
@click.option("--user_id", default=0, type=int, help="The user ID")
@click.option("--project_id", default="0", help="The project ID")
@click.option("--node_id", default=None, help="The node ID or nothing")
def main(job_id: str, user_id: str, project_id: str, node_id: str) -> List[str]:

    log.info(
        "STARTING task processing for user %s, project %s, node %s",
        user_id,
        project_id,
        node_id,
    )
    try:
        next_task_nodes = wrap_async_call(
            run_sidecar(job_id, user_id, project_id, node_id=node_id)
        )
        log.info(
            "COMPLETED task processing for user %s, project %s, node %s",
            user_id,
            project_id,
            node_id,
        )
        return next_task_nodes
    except Exception:  # pylint: disable=broad-except
        log.exception("Uncaught exception")


async def run_sidecar(
    job_id: str, user_id: str, project_id: str, node_id: str
) -> List[str]:

    async with DBContextManager() as db_engine:
        async with RabbitMQ(config=RABBIT_CONFIG) as rabbit_mq:
            next_task_nodes = await inspect(
                db_engine, rabbit_mq, job_id, user_id, project_id, node_id=node_id
            )
            log.info(
                "COMPLETED task processing for user %s, project %s, node %s",
                user_id,
                project_id,
                node_id,
            )
            return next_task_nodes
