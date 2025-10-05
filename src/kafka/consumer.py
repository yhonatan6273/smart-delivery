from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
import os
from dotenv import load_dotenv
from src.utils.google_map import get_directions
from src.services.prediction_service import prediction_service
from src.schemas.prediction import DeliveryFeatures 
from pydantic import ValidationError
from src.db.database import SessionLocal 
from src.models.models import Delivery 
from confluent_kafka.serialization import SerializationContext, MessageField

#load environment variables from .env file
load_dotenv()

#get the environment variables
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC_CALCULATE_ROUTE")
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")





#setup connection to schema registry
schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}

#this will allow us to connect to the schema registry and fetch the schemas
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

#this will deserialize the Avro messages
#it will take the raw bytes and convert them to a python dictionary
avro_deserializer = AvroDeserializer(schema_registry_client)


#this configuration is required to connect to the Kafka broker and consume messages

consumer_conf = {
    #address of the Kafka broker
    "bootstrap.servers": KAFKA_BROKER,
    #name of the consumer group
    "group.id": "route-consumer-group",      
    #where to start reading messages if no offset is committed for this group
    "auto.offset.reset": "earliest",

}

#create new consumer instance 
consumer = Consumer(consumer_conf)
#the consumer will start subscribe to the topic
consumer.subscribe([KAFKA_TOPIC])

print("Kafka Avro consumer started and listening for new deliveries...")

#this function will update the delivery in the database with the predicted eta 

def update_delivery_in_db(delivery_id: int, predicted_eta: float):
    #create a new database session
    db_session = SessionLocal()
    #try to update the delivery
    try:
        
        delivery = db_session.query(Delivery).filter(Delivery.id == delivery_id).first()

        if delivery:
            #update the field with our prediction
            delivery.predicted_eta_minutes = predicted_eta
            db_session.commit()
            print(f"Successfully updated delivery {delivery_id} in DB.")
            
        else:
            print(f"Could not find delivery {delivery_id} to update.")
            
    finally:
        #closing the session
        db_session.close()

#try to consume messages from the topic
try:
    while True:
        #Wait up to 1 second for a message if there is not any message it will return None
        msg = consumer.poll(1.0)  
        #if no message is received, continue to the next iteration of the loop
        if msg is None:
            continue  
        #if there is an error in the message, print the error and continue to the next iteration of the loop
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f" Consumer error: {msg.error()}")
                continue
        #try to process the message
        try:
            #get the raw message value and the context
            raw_message_value = msg.value()
            context = SerializationContext(msg.topic(), MessageField.VALUE)
            #deserialize the message value to a python dictionary
            delivery_data = avro_deserializer(raw_message_value, context)
            print(f"New delivery received: {delivery_data}")
            
            directions = get_directions("Tel Aviv", delivery_data["destination_address"])
            if directions is None:
                print(f"Could not calculate route for delivery ID {delivery_data.get('id')}. Skipping.")
                continue
            distance_km = float(directions['distance'].split(' ')[0])
            duration_minutes = float(directions['duration'].split(' ')[0])
            #get the features required for the prediction
            features_for_prediction = DeliveryFeatures(
                distance_km=distance_km,
                maps_eta_minutes=duration_minutes,
                hour_of_day=delivery_data.get("hour_of_day"),
                day_of_week=delivery_data.get("day_of_week")
            )
            #make the prediction using the prediction service
            predicted_eta = prediction_service.predict(features_for_prediction)
            
            print("ML prediction result")
            print(f"Google Maps ETA: {duration_minutes:.2f} minutes")
            print(f"Smart Predicted ETA: {predicted_eta:.2f} minutes")
            
            delivery_id = delivery_data.get("id")
            if delivery_id:
                predicted_eta_as_float = float(predicted_eta)
                update_delivery_in_db(delivery_id=delivery_id, predicted_eta=predicted_eta_as_float)
            else:
                print("No delivery id in message, cannot update the database.")

        except (ValidationError, Exception) as e:
            print(f"error while processing message: {e}")

except KeyboardInterrupt:
    print("Consumer stopped manually")
finally:
    consumer.close()