from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:Password@localhost/test",echo=True)
Sessionlocal = sessionmaker(autoflush=False,expire_on_commit=False,bind=engine)
SQLALCHEMY_SILENCE_UBER_WARNING=1
Base = declarative_base()