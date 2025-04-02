from dataclasses import dataclass

import aio_pika

from src.settings.settings_all import settings


@dataclass
class BrokerConsumer:
    amqp_url: str = settings.AMQP_BROKER_URL
    queue_name: str = "email_queue"

    async def open_connection(self) -> None:
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(
            self.queue_name, durable=True
        )

    async def close_connection(self) -> None:
        await self.connection.close()

    async def consume_callback_message(self) -> None:
        await self.open_connection()
        try:
            async with self.queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        print(f"Recieved message: {message.body.decode()}")
        finally:
            await self.close_connection()
