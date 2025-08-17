from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
import os
from dotenv import load_dotenv
from src.utils.google_map import get_directions


load_dotenv()

#Kafka topic name – the "channel" to listen to
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC_CALCULATE_ROUTE")
#Kafka broker address – internal Docker network hostname:port
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
#Schema Registry – needed to deserialize Avro data
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")


#Setup connection to Schema Registry
schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

#Deserialize Avro-encoded messages to dicts
avro_deserializer = AvroDeserializer(
    schema_registry_client=schema_registry_client,
    return_record_name=False 
)

#Kafka consumer configuration
consumer_conf = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "route-consumer-group",      #Consumer group ID
    "auto.offset.reset": "earliest"
}

#Create consumer instance and subscribe to the topic
consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])

print(" Kafka Avro consumer started and listening for new deliveries...")

#The main loop, consume messages continuously
try:
    while True:
        msg = consumer.poll(1.0)  #Wait up to 1 second for a message

        if msg is None:
            continue  # No message received yet
        if msg.error():
            print(f" Consumer error: {msg.error()}")
            continue

        try:
            #Deserialize the Avro-encoded message into a python dict
            delivery_data = avro_deserializer(msg.value(), None)

            print(f" New delivery received: {delivery_data}")

            #Use the function get_direction from src.utils.google_maps  to calculate the route
            directions = get_directions(
                "Tel Aviv",
                delivery_data["destination_address"]
            )

            #Log the result
            print(f" Route calculated: {directions['distance']} | Duration: {directions['duration']}")

        except Exception as e:
            print(f" Error while processing message: {e}")

except KeyboardInterrupt:
    print("Consumer stopped manually")

finally:
    consumer.close()  #close the Kafka connection
