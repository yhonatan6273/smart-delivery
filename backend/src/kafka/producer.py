from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import avro
import os
from dotenv import load_dotenv
import logging



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

KAFKA_TOPIC_REQUESTS = os.getenv("KAFKA_TOPIC_REQUESTS")
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")



#schema for the key
key_schema_str = """
{
   "name": "Key",
   "type": "string"
}
"""
#we load the schema from the json string to avro schema object
key_schema = avro.loads(key_schema_str)



# Define the schema for the message
value_schema_str = """
{
   "namespace": "delivery",
   "type": "record",
   "name": "DeliveryMessage",
   "fields" : [
        {"name": "id", "type": "int"},
        {"name": "destination_address", "type": "string"},
        {"name": "origin_address", "type": "string", "default": "tel aviv dizengoff center"},
        {"name": "hour_of_day", "type": "int"},
        {"name": "day_of_week", "type": "int"}
   ]
}
"""

#we load the schema from the json string to avro schema object
value_schema = avro.loads(value_schema_str)



#configure the avroProducer
producer_config = {
    'bootstrap.servers': KAFKA_BROKER,
    'schema.registry.url': SCHEMA_REGISTRY_URL,
    'retries': 5,
    'linger.ms': 50,
    'batch.num.messages': 100
    }

    
#create the AvroProducer instance
producer = AvroProducer(
    config=producer_config,
    default_value_schema=value_schema,
    default_key_schema=key_schema
)


#Callback function to handle delivery reports
def delivery_report(err, msg):
    
    if err is not None:
         logging.error(f"PRODUCER ERROR: message delivery failed: {err}")


         
#Function to send delivery request to kafka topic
def send_delivery_request(delivery_data: dict):
   
    payload = {
        "id": delivery_data["id"],
        "destination_address": delivery_data["destination_address"],
        "origin_address": delivery_data.get("origin_address", "tel aviv dizengoff center"),
        "hour_of_day": delivery_data["hour_of_day"],
        "day_of_week": delivery_data["day_of_week"]
    }
   
    producer.produce(topic=KAFKA_TOPIC_REQUESTS , key=str(payload["id"]), value=payload)
    #Check if kafka received the message and the message is saved successfully in the topic
    producer.poll(0)
    logging.info(f"Sent request for Delivery ID: {payload['id']}")