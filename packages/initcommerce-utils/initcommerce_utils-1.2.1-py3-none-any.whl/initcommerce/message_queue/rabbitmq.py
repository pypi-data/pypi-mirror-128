import asyncio

import aio_pika
from aio_pika import Channel  # noqa: F401
from aio_pika import Connection as MessageQueue  # noqa: F401
from aio_pika import IncomingMessage, Message  # noqa: F401


async def get_message_queue(url: str, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    _connection = await aio_pika.connect_robust(url, loop=loop)

    return _connection
