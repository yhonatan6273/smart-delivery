from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import avro
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC_CALCULATE_ROUTE")
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")



# Define the schema for the message
value_schema_str = """
{
   "namespace": "delivery",
   "type": "record",
   "name": "DeliveryMessage",
   "fields" : [
        {"name": "id", "type": "int"},
        {"name": "user_id", "type": "int"},
        {"name": "customer_id", "type": "string"},
        {"name": "customer_name", "type": "string"},
        {"name": "customer_phone", "type": "string"},
        {"name": "destination_address", "type": "string"},
        {"name": "delivery_type", "type": "string"},
        {"name": "status", "type": "string", "default": "approve"},
        {"name": "origin_address", "type": "string", "default": "Tel Aviv"}
   ]
}
"""

value_schema = avro.loads(value_schema_str)

producer_config = {
    'bootstrap.servers': KAFKA_BROKER,
    'schema.registry.url': SCHEMA_REGISTRY_URL,
    'linger.ms': 50,
    'batch.num.messages': 100
    }

    

producer = AvroProducer(
    config=producer_config,
    default_value_schema=value_schema
)


def send_delivery_report_avro(delivery_data: dict):
    try:
        producer.produce(topic=KAFKA_TOPIC, value=delivery_data)
        producer.poll(0)
        producer.flush()
        print(f"Produced message to topic {KAFKA_TOPIC}")
    except SerializerError as e:
        print(f"Message serialization failed: {e}")
