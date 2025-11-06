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
        {"name": "origin_address", "type": "string", "default": "Tel Aviv"},
         {"name": "hour_of_day", "type": "int"},
        {"name": "day_of_week", "type": "int"}
   ]
}
"""
#we load the schema from the string
value_schema = avro.loads(value_schema_str)
#configure the avroProducer
producer_config = {
    'bootstrap.servers': KAFKA_BROKER,
    'schema.registry.url': SCHEMA_REGISTRY_URL,
    'linger.ms': 50,
    'batch.num.messages': 100
    }

    
#create the AvroProducer instance
producer = AvroProducer(
    config=producer_config,
    default_value_schema=value_schema
)


#callback function to handle delivery reports
def delivery_report(err, msg):
    
    if err is not None:
        print(f"PRODUCER ERROR: message delivery failed: {err}")

        
#this function sends the delivery data to kafka topic
def send_delivery_report_avro(delivery_data: dict):
    #try to produce the message
    try:
      
        producer.produce(
            topic=KAFKA_TOPIC, 
            value=delivery_data, 
            on_delivery=delivery_report
        )

     
        producer.poll(0)
    #if the internal queue is full, we can try to flush it and retry after 10 seconds
    except BufferError:
        print("--- PRODUCER ERROR: Local producer queue is full. Flushing... ---")
        
        producer.flush(10) 

    except SerializerError as e:
        print(f"PRODUCER ERROR: message serialization failed: {e}")

remaining_messages = producer.flush(10) 
if remaining_messages > 0:
    print(f"PRODUCER WARNING: {remaining_messages} messages still in queue after flush.")
