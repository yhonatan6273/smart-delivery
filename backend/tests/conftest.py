from fastapi.testclient import TestClient
from src.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv
from src.db.database import get_db,Base
import pytest
from src.auth.oauth2 import create_access_token
from src.models import models
from src.utils.UtilsLogin import hash_password
from confluent_kafka import avro
from confluent_kafka.admin import AdminClient
from confluent_kafka.avro import AvroProducer, AvroConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
import time
from src.kafka.producer import value_schema_str
from src.kafka.producer import key_schema_str
import logging
from src.kafka.admin import create_topic_init
from sqlalchemy.pool import NullPool


log = logging.getLogger(__name__)
load_dotenv(".env.test")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

KAFKA_TEST_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
SCHEMA_REGISTRY_TEST_URL = os.getenv("SCHEMA_REGISTRY_URL")
KAFKA_TOPIC_REQUESTS = os.getenv("KAFKA_TOPIC_REQUESTS")
KAFKA_TOPIC_RESULTS = os.getenv("KAFKA_TOPIC_RESULT")
VALUE_SCHEMA = avro.loads(value_schema_str)
KEY_SCHEMA = avro.loads(key_schema_str)
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}"

#DATA BASE Fixtures

#engine is the connection to the database poolclass=NullPool to avoid connection issues in tests
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
#this will create a new session for the database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#fixture for the database session
@pytest.fixture
def session():
    #dropping all current tables and creating new ones for a clean test environment
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #creating the test database session 
    db = TestingSessionLocal()
    #trying to yield the database session to the tests
    try:
        yield db
    finally:
        db.close()
#fixture for the test client
@pytest.fixture
def client(session):
   #overriding the get_db dependency to use the test database session
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overrid_get_db
    #creating a test client to simulate requests to the FastAPI app
    yield TestClient(app)




#creating a test user fixture to be used in tests
@pytest.fixture
def test_user(client):
    user_data = {"email": "testuser@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201, f"Could not create user. Status: {res.status_code}, Body: {res.text}"
    new_user = res.json()
    new_user['password'] = user_data['password'] 
    return new_user

#creating a test admin user fixture to be used in tests
#we need to create the admin user directly in the database because the /users endpoint creates only normal users
@pytest.fixture
def test_admin_user(session):
    plain_password = "password123"
    hashed_password = hash_password(plain_password)
    new_admin = models.User(email="testuseradmin@gmail.com", password=hashed_password, role="admin")
    
    session.add(new_admin)
    session.commit()
    session.refresh(new_admin)

    return {
        "id": new_admin.id,
        "email": new_admin.email,
        "role": new_admin.role,
        "created_at": new_admin.created_at
      
    }

#creating a token fixture to be used in authorized client tests
@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id'],"role": test_user['role']})


#creating a token fixture for the admin user to be used in authorized admin client tests
@pytest.fixture
def token_admin(test_admin_user):
    return create_access_token(data={"user_id": test_admin_user['id'],"role": test_admin_user['role']})


#creating a authorized client fixture to be used in authorized requests tests
#the authorized client will have the token in the headers and will be able to access protected routes
@pytest.fixture
def authorized_client(client, token):
    client.headers.update({
        "Authorization": f"Bearer {token}"
    })
    return client

#creating a authorized admin client fixture to be used in authorized requests tests
@pytest.fixture
def authorized_admin_client(client, token_admin):
    client.headers.update({
        **client.headers,
        "Authorization": f"Bearer {token_admin}"
    })
    return client

#creating a test deliveries fixture to be used in tests
@pytest.fixture
def test_deliveries(session, test_user, test_admin_user):
    session.add_all([models.Delivery(customer_id="12345678", delivery_type="express", customer_phone="+972541234567", customer_name="John Doe", 
                                     customer_address="tel aviv", manager_phone="053-9236230", status="approve", user_id=test_user['id']),
                     models.Delivery(customer_id="87654321", delivery_type="standard", customer_phone="+972598765432", customer_name="Jane Smith",
                                     customer_address="haifa", manager_phone="053-9236230", status="approve", user_id=test_user['id'],predicted_eta_minutes=30.0),
                        models.Delivery(customer_id="11223344", delivery_type="express", customer_phone="+972512345678", customer_name="Alice Johnson",
                                     customer_address="tel aviv", manager_phone="053-9236230", status="approve", user_id=test_admin_user['id']),
                        models.Delivery(customer_id="44332211", delivery_type="standard", customer_phone="+972576543210", customer_name="Bob Brown",
                                     customer_address="haifa", manager_phone="053-9236230", status="approve", user_id=test_admin_user['id'],predicted_eta_minutes=45.0)
                     ])
    session.commit()
    return session.query(models.Delivery).all()


#KAFKA Fixtures

#fixture to set up the Kafka test environment (runs once per session)
#it waits for the broker and schema registry to be available and creates the test topic
@pytest.fixture(scope="session")
def kafka_test_service():
   
    admin_client = AdminClient({'bootstrap.servers': KAFKA_TEST_BROKER})
    retries = 10
    broker_ready = False
    while retries > 0:
        try:
            admin_client.list_topics(timeout=5)
            log.info("kafka Broker is ready.")
            broker_ready = True
            break
        except Exception:
            log.info(f"waiting for Kafka Broker ({retries} retries left)")
            retries -= 1
            time.sleep(5)
    if not broker_ready:
        pytest.fail("Could not connect to Kafka Broker for tests.")

    sr_client = SchemaRegistryClient({'url': SCHEMA_REGISTRY_TEST_URL})
    retries = 10
    sr_ready = False
    while retries > 0:
        try:
            sr_client.get_subjects()
            log.info("schema Registry is ready.")
            sr_ready = True
            break
        except Exception:
            log.info(f"waiting for schema registry ({retries} retries left)")
            retries -= 1
            time.sleep(5)
    if not sr_ready:
        pytest.fail("Could not connect to Schema Registry for tests.")

    #create the test topic
    log.info("Initializing topics using existing admin logic...")
    try:
        create_topic_init()
    except Exception as e:
        log.error(f"Error during topic initialization: {e}")
       
    yield



# Fixture for a producer to send messages setup data during tests
@pytest.fixture
def kafka_producer():
    producer_config = {
        'bootstrap.servers': KAFKA_TEST_BROKER,
        'schema.registry.url': SCHEMA_REGISTRY_TEST_URL,
    }
    producer = AvroProducer(producer_config,default_key_schema=KEY_SCHEMA, default_value_schema=VALUE_SCHEMA)
    yield producer
    producer.flush(10)



# Fixture for a raw consumer to verify messages sent by your application
@pytest.fixture
def kafka_consumer():
    conf = {
        'bootstrap.servers': KAFKA_TEST_BROKER,
        'group.id': 'test-verification-group',
        'auto.offset.reset': 'earliest',
        'schema.registry.url': SCHEMA_REGISTRY_TEST_URL
    }
    consumer = AvroConsumer(conf)
    
    # We allow the consumer to subscribe dynamically in the test
    yield consumer
    consumer.close()