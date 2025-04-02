import uuid
from dataclasses import dataclass

from src.broker.producer import BrokerProducer


@dataclass
class MailClient:
    broker_producer: BrokerProducer

    async def send_welcome_email(self, to: str) -> None:
        email_body = {
            "message": "Welocome to pomodoro",
            "user_email": to,
            "subject": "Welcome message",
            "correlation_id": str(uuid.uuid4()),
        }

        await self.broker_producer.send_welcome_email(data=email_body)
        return
