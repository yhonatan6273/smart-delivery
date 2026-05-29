import os
import json
import logging
from dotenv import load_dotenv
from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
from src.utils.google_map import get_directions
from src.schemas.prediction import DeliveryFeatures 
from src.services.prediction_service import prediction_service



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()


KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")
KAFKA_TOPIC_REQUESTS = os.getenv("KAFKA_TOPIC_REQUESTS") 
KAFKA_TOPIC_RESULTS = os.getenv("KAFKA_TOPIC_RESULT") 






schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}

schema_registry_client = SchemaRegistryClient(schema_registry_conf)
#transformer from avro to python dict
avro_deserializer = AvroDeserializer(schema_registry_client)


consumer_conf = {
    #to which broker to connect for getting messages 
    "bootstrap.servers": KAFKA_BROKER,
    #the group name
    "group.id": "ml-prediction-group",
    #we want to read all messages from the beginning of the topic when we start the consumer for the first time
    "auto.offset.reset": "earliest",
    #control when the consumer commits the offsets of messages it has processed
    "enable.auto.commit": False,
}
#to witch broker to send messages 
producer_conf = {
    "bootstrap.servers": KAFKA_BROKER,
    "retries": 5,
}

# Function to process messages and respond with predictions
def process_and_respond():
    #create the consumer
    consumer = Consumer(consumer_conf)
    #to which topic to listen
    consumer.subscribe([KAFKA_TOPIC_REQUESTS])
    #create the producer
    producer = Producer(producer_conf)

    logging.info("ML Service Started Listening.")

    while True:
        # consumer will go to the topic to see if there are new messages and will wait for 1 second
        msg = consumer.poll(1.0)
        
        if msg is None: 
            continue
        
        if msg.error():
            #check if the error is a end of partition event
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logging.error(f"Consumer error: {msg.error()}")
                continue

        try:
            # Deserialize the incoming Avro message
            context = SerializationContext(msg.topic(), MessageField.VALUE)
            data = avro_deserializer(msg.value(), context)
            
            delivery_id = data.get('id')
            logging.info(f"Processing delivery request ID: {delivery_id}")

            # Get Data from Google Maps
            # We use the origin address if provided, otherwise default to tel aviv dizengoff center
            origin = data.get("origin_address", "tel aviv dizengoff center")
            destination = data.get("destination_address")
            
            directions = get_directions(origin, destination)
            
            if not directions:
                logging.warning(f"Failed to get directions for ID {delivery_id}. Skipping.")
                continue 

           
            d_km = float(directions['distance'].split(' ')[0])
            duration_minutes = float(directions['duration'].split(' ')[0])

            # Prepare features for the ML model
            features = DeliveryFeatures(
                distance_km=d_km,
                maps_eta_minutes=duration_minutes,
                hour_of_day=data["hour_of_day"],
                day_of_week=data["day_of_week"]
            )
            
            # Run the ML Prediction
           
            predicted_eta = prediction_service.predict(features)
            
            # Prepare and Send Response
            result_payload = {
                "id": delivery_id,
                #not allowing negative eta
                "predicted_eta": max(0.0, float(predicted_eta)),
                "maps_eta": duration_minutes 
            }

            # Send the result back to the results topic as JSON
            producer.produce(
                topic= KAFKA_TOPIC_RESULTS, 
                key=str(delivery_id),
                value=json.dumps(result_payload)
            )
            
            #Ensure the message is sent
            producer.poll(0)
            logging.info(f"Sent Result for ID {delivery_id}: {predicted_eta} min")
            
            #approve the message as processed
            consumer.commit(asynchronous=False)
            logging.info(f"Successfully processed, sent, and committed ID {delivery_id}")

        except Exception as e:
            logging.error(f"Error in ML loop: {e}")

if __name__ == "__main__":
    process_and_respond()