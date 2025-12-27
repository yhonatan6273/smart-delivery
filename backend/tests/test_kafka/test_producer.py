from src.kafka.producer import send_delivery_request
import os

KAFKA_TOPIC_REQUESTS = os.getenv("KAFKA_TOPIC_REQUESTS")



# Function to test the send_delivery_request function
def test_send_delivery_request(kafka_consumer):
   
    kafka_consumer.subscribe([KAFKA_TOPIC_REQUESTS])

    # Prepare test data
    target_id = 12345
    delivery_data = {
        "id": target_id,
        "destination_address": "Haifa",
        "origin_address": "Tel aviv dizengoff center",
        "hour_of_day": 14,
        "day_of_week": 2
    }

    # Call the function under test
    send_delivery_request(delivery_data)

    
    found_message = None
    
    # Poll the consumer for messages
    for _ in range(20):
        msg = kafka_consumer.poll(1.0)
        
        if msg is None:
            continue
        if msg.error():
            continue
            
        received_value = msg.value()
        
        #check if this is the message we are looking for
        if received_value['id'] == target_id:
            found_message = received_value
            break 
        


    # Assertions
    assert found_message is not None, f"Timeout: Message with ID {target_id} was not found in Kafka."

   
    assert found_message['id'] == delivery_data['id']
    assert found_message['destination_address'] == delivery_data['destination_address']
    assert found_message['hour_of_day'] == delivery_data['hour_of_day']