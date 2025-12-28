import pytest
from unittest.mock import MagicMock, patch
import json
import os
from src.kafka.ml_consumer import process_and_respond


class StopLoopException(Exception):
    pass

@pytest.mark.ml
# Patching necessary components in the ml_consumer module
@patch("src.kafka.ml_consumer.get_directions")
@patch("src.kafka.ml_consumer.prediction_service")
@patch("src.kafka.ml_consumer.Consumer")
@patch("src.kafka.ml_consumer.Producer")
@patch("src.kafka.ml_consumer.avro_deserializer") 


# Function to test the full ML consumer flow
def test_ml_consumer_flow(mock_deserializer, mock_producer_cls, mock_consumer_cls, mock_prediction_service, mock_get_directions):

    # Mock Google Maps
    mock_get_directions.return_value = {
        'distance': '10 km',
        'duration': '15 mins'
    }
    
    # Mock Prediction Service
    mock_prediction_service.predict.return_value = 25.5
    
    # Mock Kafka Consumer
    mock_consumer_instance = mock_consumer_cls.return_value
    
    # crating fake message
    mock_msg = MagicMock()
    mock_msg.error.return_value = None
    mock_msg.topic.return_value = "requests_topic"
    mock_msg.value.return_value = b"dummy_bytes"

    # Setting up the poll side effect to return our mock message once, then raise StopLoopException to exit the loop
    mock_consumer_instance.poll.side_effect = [mock_msg, StopLoopException("Stop Loop")]
    
    # Mock Avro Deserializer
    mock_deserializer.return_value = {
        "id": 999,
        "destination_address": "Eilat",
        "origin_address": "Tel aviv dizengoff center",
        "hour_of_day": 10,
        "day_of_week": 1
    }

    # Mock Kafka Producer
    mock_producer_instance = mock_producer_cls.return_value

    # Execute the consumer processing loop 
    try:
        process_and_respond()
    except StopLoopException:
        pass
    except Exception as e:
        pytest.fail(f"Test failed with unexpected error: {e}")

    #check that the mocked functions were called as expected
    mock_get_directions.assert_called_once()
    mock_prediction_service.predict.assert_called_once()
    
    #check that the Producer was called
    assert mock_producer_instance.produce.called, "Producer.produce was never called!"
    
    # Extract the arguments with which produce was called
    args, kwargs = mock_producer_instance.produce.call_args
    
    topic = kwargs.get('topic')
    key = kwargs.get('key')
    value = kwargs.get('value')
    
    # Deserialize the value for easier assertions
    payload = json.loads(value)
   
    expected_topic = os.getenv("KAFKA_TOPIC_RESULT", "delivery_results")


    # Assertions
    assert topic == expected_topic, f"Topic mismatch! Expected: {expected_topic}, Got: {topic}"
    assert key == "999", "Key mismatch!"
    assert payload['id'] == 999
    assert payload['predicted_eta'] == 25.5
    assert payload['maps_eta'] == 15.0 