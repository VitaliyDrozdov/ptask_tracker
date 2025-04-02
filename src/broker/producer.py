import json
from dataclasses import dataclass

import aio_pika


@dataclass
class BrokerProducer:
    amqp_url: str
    email_queue: str = "email_queue"

    async def open_connection(self) -> None:
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(self.email_queue, durable=True)

    async def close_connection(self) -> None:
        await self.connection.close()

    async def send_welcome_email(self, data: dict) -> None:
        await self.open_connection()
        try:
            body = json.dumps(data).encode()
            message = aio_pika.Message(body=body)
            await self.channel.default_exchange.publish(
                message=message, routing_key=self.email_queue
            )
            print(f"Message sent to queue: {self.email_queue}")
        finally:
            await self.close_connection()
