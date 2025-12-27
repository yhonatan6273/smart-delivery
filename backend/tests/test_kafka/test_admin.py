from confluent_kafka.admin import AdminClient
import os
from src.kafka.admin import create_topic_init


KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC_REQUESTS = os.getenv("KAFKA_TOPIC_REQUESTS")
KAFKA_TOPIC_RESULTS = os.getenv("KAFKA_TOPIC_RESULT")

# Function to test the Kafka topic creation
def test_create_topic_init(kafka_test_service):
   
    #crate the topics
    create_topic_init()
    
    #connect to kafka
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BROKER})
    cluster_metadata = admin_client.list_topics(timeout=10)
    
    topics = list(cluster_metadata.topics.keys())
   

 
    assert KAFKA_TOPIC_REQUESTS in topics
    assert KAFKA_TOPIC_RESULTS in topics