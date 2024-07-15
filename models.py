from sqlalchemy import String,Column,Integer
from database import Base

class Tweet(Base):
    __tablename__ =  'Tweets'
    id=Column(Integer,primary_key = True)
    tweet=Column(String(255),nullable=False)
    uploader = Column(String(255),nullable = False)
    likes = Column(Integer,default = 0)
    
    def __repr__(self) -> str:
        return f"<Tweet tweet={self.tweet} uploader={self.uploader} likes = {self.likes}>"