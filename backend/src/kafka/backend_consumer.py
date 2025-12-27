from confluent_kafka import Consumer
import json
import os
from src.db.database import SessionLocal 
from src.models.models import Delivery 
import logging




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC_RESULTS = os.getenv("KAFKA_TOPIC_RESULT") 

# Configure the consumer to read from the results topic
consumer_conf = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "backend-updater-group",
    "auto.offset.reset": "earliest",
}

# Function to consume messages and update the database
def update_db_loop():
    #create the consumer
    consumer = Consumer(consumer_conf)
    consumer.subscribe([KAFKA_TOPIC_RESULTS])
    
    logging.info("Backend Updater Started.")

    while True:
        # Poll for new messages from the topic
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error(): continue
        #open new connection to the DB
        session = SessionLocal()
        try:
            
            data = json.loads(msg.value().decode('utf-8'))
            delivery_id = data["id"]
            eta = data["predicted_eta"]

            #upgrade the DB
            delivery = session.query(Delivery).filter(Delivery.id == delivery_id).first()
            if delivery:
                delivery.predicted_eta_minutes = eta
                session.commit()
                logging.info(f"Updated DB: Delivery {delivery_id} -> ETA {eta}")
            
        except Exception as e:
            logging.error(f"Error updating DB: {e}")
            session.rollback()
        finally:
            session.close()
# Run only if this script is executed directly
if __name__ == "__main__":
    update_db_loop()