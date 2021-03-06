# pylint: disable=unused-argument

import json
from typing import List

import aio_pika

from simcore_sdk.config.rabbit import Config
from simcore_service_sidecar.rabbitmq import RabbitMQ

core_services = ["rabbit"]


async def test_rabbitmq(
    loop, rabbit_config: Config, rabbit_queue: aio_pika.Queue, mocker
):
    rabbit = RabbitMQ()
    assert rabbit

    mock_close_connection_cb = mocker.patch(
        "simcore_service_sidecar.rabbitmq._close_callback"
    )
    mock_close_channel_cb = mocker.patch(
        "simcore_service_sidecar.rabbitmq._channel_close_callback"
    )
    mock_reconnect_cb = mocker.patch(
        "simcore_service_sidecar.rabbitmq._reconnect_callback"
    )

    user_id: str = "some user id"
    project_id: str = "some project id"
    node_id: str = "some node id"
    progress_msg: str = "I progressed a lot since last time"
    log_msg: str = "I am logging"
    log_messages: List[str] = ["I", "am a logger", "man..."]

    incoming_data = []

    async def rabbit_message_handler(message: aio_pika.IncomingMessage):
        data = json.loads(message.body)
        incoming_data.append(data)

    await rabbit_queue.consume(rabbit_message_handler, exclusive=True, no_ack=True)

    async with RabbitMQ(config=rabbit_config) as rabbitmq:
        assert rabbitmq.connection.ready

        await rabbitmq.post_log_message(user_id, project_id, node_id, log_msg)
        await rabbitmq.post_log_message(user_id, project_id, node_id, log_messages)
        await rabbitmq.post_progress_message(user_id, project_id, node_id, progress_msg)

    mock_close_channel_cb.assert_called_once()
    mock_close_connection_cb.assert_called_once()
    mock_reconnect_cb.assert_not_called()

    assert len(incoming_data) == 3

    assert incoming_data[0] == {
        "Channel": "Log",
        "Messages": [log_msg],
        "Node": node_id,
        "project_id": project_id,
        "user_id": user_id,
    }
    assert incoming_data[1] == {
        "Channel": "Log",
        "Messages": ["I", "am a logger", "man..."],
        "Node": "some node id",
        "project_id": "some project id",
        "user_id": "some user id",
    }
    assert incoming_data[2] == {
        "Channel": "Progress",
        "Node": "some node id",
        "Progress": "I progressed a lot since last time",
        "project_id": "some project id",
        "user_id": "some user id",
    }
