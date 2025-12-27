import logging
from confluent_kafka.admin import AdminClient, NewTopic
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Function to create kafka topics
def create_topic_init():
    broker = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    topic_requests = os.getenv("KAFKA_TOPIC_REQUESTS")
    topic_results = os.getenv("KAFKA_TOPIC_RESULT")
   #if any of the env variables are missing, log error and return
    if not broker or not topic_requests or not topic_results:
        logging.error("Kafka environment variables are missing.")
        return

    logging.info(f"Connecting to Kafka at {broker} to manage topics")

    #creating the admin client, and give him the broker address
    admin_client = AdminClient({"bootstrap.servers": broker})
    
    #creating the partitions and replication factor for each topic
    topics_list = [
        NewTopic(topic=topic_requests, num_partitions=3, replication_factor=1),
        NewTopic(topic=topic_results, num_partitions=2, replication_factor=1)
    ]
    
    try:
        #tell the admin client to create the topics from the topics_list
        fs = admin_client.create_topics(topics_list)
        
        
        for topic, f in fs.items():
            try:
                #stop doing other things until the topic is created successfully or fails
                f.result()  
                logging.info(f" Topic '{topic}' created successfully.")
            except Exception as e:  
                #check if the error is topic already exists 
                if "Topic" in str(e) and "already exists" in str(e):
                    logging.info(f"Topic '{topic}' already exists. No action needed.")
                else:
                    logging.error(f"Failed to create topic '{topic}': {e}")
                
    except Exception as e:
        logging.error(f"Failed to init Kafka topics. {e}")