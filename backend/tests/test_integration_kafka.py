# tests/test_integration_kafka.py
from unittest.mock import patch
from src.models.models import Delivery
from src.kafka.consumer import process_message
from tests.conftest import KAFKA_TEST_TOPIC

#patches the KAFKA_TOPIC constant in the Producer module.
#this will redirect messages sent from the API to the test topic instead of the production one.
@patch("src.kafka.producer.KAFKA_TOPIC", KAFKA_TEST_TOPIC)
#verifies that creating a new delivery from the API 
#successfully sends a valid message to the corresponding Kafka topic.
def test_create_delivery_sends_kafka_message(authorized_client, avro_consumer, test_user):
    api_payload = {
        "customer_id": "12345678",
        "customer_name": "Test Customer",
        "customer_phone": "+972541234567",
        "customer_address": "tel aviv", 
        "delivery_type": "express"
    }
    response = authorized_client.post("/deliveries", json=api_payload)
    assert response.status_code == 201
    #check for the new message in the kafka topic (wait in the topic for up to 10 seconds)
    msg = avro_consumer.poll(timeout=10.0)
    assert msg is not None, "consumer did not receive any message."
    assert not msg.error(), f"consumer received an error: {msg.error()}"
    
    message_data = msg.value()
    assert message_data["customer_id"] == api_payload["customer_id"]
    assert message_data["user_id"] == test_user['id']
   
# Patches the get_directions function to prevent a real network API call from google map
#instead, the function will return a predefined value that we set in the test.
#and Patches the ML model prediction function.
#the purpose is to isolate the consumers logic from the model itself and to control the predicted value for the test.
@patch("src.kafka.consumer.get_directions")
#and Patches the ML model prediction function.
#we will isolate the consumers logic from the model itself and to control the predicted value for the test.
@patch("src.kafka.consumer.prediction_service.predict")
#verifies that the process_message function correctly processes an incoming message and updates the database as we expected.
def test_consumer_logic_updates_db(mock_predict, mock_get_directions, session, test_user):
    #setting the mocked return values for the patched functions
    mock_get_directions.return_value = {'distance': '15.0 km', 'duration': '25.0 minutes'}
    mock_predict.return_value = 35.5
    #creating an initial delivery record in the database with a null predicted_eta
    delivery_to_update = Delivery(
        id=202, user_id=test_user['id'], customer_id="cust-456",
        customer_address="Haifa", delivery_type="standard", customer_name="Jane Doe",
        customer_phone="987654321", status="approve", manager_phone="053-9236230"
    )
    session.add(delivery_to_update)
    session.commit()
    delivery_before = session.query(Delivery).filter(Delivery.id == 202).one()
    assert delivery_before.predicted_eta_minutes is None

    #preparing the mock message data to be passed to the consumers processing function
    message_data = {
        "id": delivery_to_update.id,
        "destination_address": "Haifa",
        "hour_of_day": 18,
        "day_of_week": 5
    }
    process_message(message_data, db_session=session)

    
    session.refresh(delivery_before) 
    delivery_after = delivery_before
    assert delivery_after.predicted_eta_minutes is not None
    assert delivery_after.predicted_eta_minutes == 35.5
    mock_get_directions.assert_called_once()
    