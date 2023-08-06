from microservice_template_core.tools.logger import get_logger
from microservice_template_core.settings import ServiceConfig, KafkaConfig
from confluent_kafka import Consumer

logger = get_logger()


class KafkaConsumeMessages(object):
    def __init__(self, kafka_topic):
        self.kafka_topic = kafka_topic

    def start_consumer(self):
        """
        Start consumer
        """

        logger.debug(f"Initializing Kafka Confluent Consumer - {ServiceConfig.SERVICE_NAME}. Topic - {self.kafka_topic}")

        consumer = Consumer(
            {
                'bootstrap.servers': KafkaConfig.KAFKA_SERVERS,
                'group.id': ServiceConfig.SERVICE_NAME,
                'auto.offset.reset': 'latest',
                'allow.auto.create.topics': True,
                'session.timeout.ms': KafkaConfig.consumer_session_timeout_ms,
                'heartbeat.interval.ms': KafkaConfig.consumer_heartbeat_interval_ms,
                'offset.store.method': 'broker'
            }
        )

        consumer.subscribe([self.kafka_topic])

        return consumer
