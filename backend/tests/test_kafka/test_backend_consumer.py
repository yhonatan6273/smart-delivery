
from unittest.mock import MagicMock, patch
import json
from src.models.models import Delivery
from src.kafka.backend_consumer import update_db_loop 

#custom exception to stop the infinite loop in the consumer after one iteration
class StopLoopException(Exception):
    pass

@patch("src.kafka.backend_consumer.SessionLocal") 
@patch("src.kafka.backend_consumer.Consumer")

# Function to test the backend consumer flow
def test_backend_consumer_flow(mock_consumer_cls, mock_session_local, session, test_deliveries):
   
    #connect to the mock database session
    mock_session_local.return_value = session

    #choose a delivery to update
    target_delivery = test_deliveries[0]
    target_id = target_delivery.id
    old_eta = target_delivery.predicted_eta_minutes 
    new_eta = 45.5

    #making the mock consumer
    mock_consumer = mock_consumer_cls.return_value
    mock_msg = MagicMock()
    mock_msg.error.return_value = None
    
    payload = {
        "id": target_id,
        "predicted_eta": new_eta
    }
    mock_msg.value.return_value = json.dumps(payload).encode('utf-8')

    #we want the poll to return our mock message once, then raise StopLoopException to exit the loop
    mock_consumer.poll.side_effect = [mock_msg, StopLoopException("Stop")]


    try:
        update_db_loop()
    except StopLoopException:
        pass

    #check the database for the updated delivery
    session.expire_all() 
    updated_delivery = session.query(Delivery).filter(Delivery.id == target_id).first()


    # Assertions
    assert updated_delivery.predicted_eta_minutes == new_eta