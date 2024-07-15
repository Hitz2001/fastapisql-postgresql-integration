from database import Base,engine
from models import Tweet
Base.metadata.create_all(engine)
