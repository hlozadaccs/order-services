import json
import os
from typing import Optional

from aiokafka import AIOKafkaProducer

from app.config import settings

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", settings.KAFKA_URL)


class KafkaProducerSingleton:
    _instance: Optional["KafkaProducerSingleton"] = None

    def __new__(cls, brokers=bootstrap_servers):
        if cls._instance is None:
            cls._instance = super(KafkaProducerSingleton, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, brokers=bootstrap_servers):
        if self._initialized:
            return
        self.brokers = brokers
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.brokers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self._initialized = True

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic: str, value: dict):
        await self.producer.send_and_wait(topic, value)
