from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
import logging
import os
from dotenv import load_dotenv
from src.utils.google_map import get_directions
from src.services.prediction_service import prediction_service
from src.schemas.prediction import DeliveryFeatures 
from pydantic import ValidationError
from src.db.database import SessionLocal 
from src.models.models import Delivery 
from confluent_kafka.serialization import SerializationContext, MessageField


#setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC_CALCULATE_ROUTE")
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")

#setup connection to schema registry
schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
avro_deserializer = AvroDeserializer(schema_registry_client)

#the consumer configuration for connecting to the kafka broker
consumer_conf = {
    #the server address of the kafka broker
    "bootstrap.servers": KAFKA_BROKER,
    #the name of the consumer group
    "group.id": "route-consumer-group",
    #from where to start reading messages if its new consumer group
    "auto.offset.reset": "earliest",
}

#function to update the delivery record in the database
def update_delivery_in_db(db_session, delivery_id: int, predicted_eta: float):
    try:
        delivery = db_session.query(Delivery).filter(Delivery.id == delivery_id).first()
        
        if delivery:
            delivery.predicted_eta_minutes = predicted_eta
            db_session.commit()
            logging.info(f"successfully updated delivery {delivery_id} in DB.")
        else:
            logging.info(f"could not find delivery {delivery_id} to update.")
    except Exception as e:
        logging.exception(f"DB error during update for delivery_id {delivery_id}: {e}")
        db_session.rollback()

        
#function to process each incoming message
def process_message(message_data: dict, db_session):
    delivery_id = message_data.get("id")
    try:
        logging.info(f"new delivery received: {message_data}")
        
        directions = get_directions("Tel Aviv", message_data["destination_address"])
        if directions is None:
            logging.info(f"could not calculate route for delivery ID {message_data.get('id')}. Skipping.")
            return

        distance_km = float(directions['distance'].split(' ')[0])
        duration_minutes = float(directions['duration'].split(' ')[0])
        
        features_for_prediction = DeliveryFeatures(
            distance_km=distance_km,
            maps_eta_minutes=duration_minutes,
            hour_of_day=message_data.get("hour_of_day"),
            day_of_week=message_data.get("day_of_week")
        )
        
        predicted_eta = prediction_service.predict(features_for_prediction)
        
        logging.info(f"ML prediction result for ID {delivery_id}: Smart ETA = {predicted_eta:.2f} min (Google ETA: {duration_minutes:.2f} min)")
        
        delivery_id = message_data.get("id")
        if delivery_id:
            update_delivery_in_db(db_session, delivery_id=delivery_id, predicted_eta=float(predicted_eta))
        else:
            logging.info("no delivery id in message, cannot update the database.")

    except (ValidationError, Exception) as e:
        logging.info(f"error while processing message: {e}")


#function to run the main consumer loop
#the function will continuously polls for new messages and processes them
def main_loop():
    
    consumer = Consumer(consumer_conf)
    consumer.subscribe([KAFKA_TOPIC])
    logging.info("kafka Avro consumer started and listening for new deliveries...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.info(f"Consumer error: {msg.error()}")
                    continue
            
            # Message received, now process it
            db_session = SessionLocal()
            try:
                context = SerializationContext(msg.topic(), MessageField.VALUE)
                delivery_data = avro_deserializer(msg.value(), context)
                process_message(delivery_data, db_session)
            finally:
                db_session.close()

    except KeyboardInterrupt:
        logging.infoprint("consumer stopped manually")
    finally:
        consumer.close()
        logging.info("Kafka consumer closed.")

#entry point for running the consumer
if __name__ == "__main__":
    main_loop()