import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from main import app,get_db
from database import Base
import random


SQLITE_DATABASE_URL = "sqlite:///.test_db.db"

engine = create_engine(SQLITE_DATABASE_URL,connect_args = {"check_same_thread":False},poolclass = StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    
    
@pytest.fixture(scope="function")    
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def generate_random_id():
    return random.randint(1,100000)

@pytest.fixture(scope="function")
def generate_tweet_json(generate_random_id):
    return {
        "id":generate_random_id,
        "uploader":"Shubh Shah",
        "tweet":"Uploaded in sqllite",
        "likes":5
    }