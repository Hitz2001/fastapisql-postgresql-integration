import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app,get_db
import models


SQLACHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(SQLACHEMY_DATABASE_URL,connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal();
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

