from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import List
from database import Sessionlocal
import models

app = FastAPI()


class Tweet(BaseModel):
    id:int
    uploader:str
    tweet:str
    likes:int

    class Config:
        orm_mode = True
        
    
db = Sessionlocal()

def get_db():
    db = Sessionlocal();
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/")
async def root() -> dict:
    return {"message":"Hello world!"}

@app.get('/tweets',response_model = List[Tweet],status_code = 200)
def get_all_tweets() -> List[models.Tweet]:
    items = db.query(models.Tweet).all()
    return items

@app.get('/tweet/{id}',response_model = Tweet,status_code=status.HTTP_200_OK)
def get_tweet_by_id(id:int) -> models.Tweet:
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if tweet is None:
        raise HTTPException(status_code=404,detail = "Tweet not found")
    else:
        return tweet

@app.post('/tweet',response_model=Tweet,status_code=status.HTTP_201_CREATED)
def create_tweet(item:Tweet) -> models.Tweet:
    new_tweet = models.Tweet(tweet = item.tweet,uploader = item.uploader,likes = item.likes,id = item.id)
    db_tweet = db.query(models.Tweet).filter(item.id == models.Tweet.id).first()
    if db_tweet is not None:
        raise HTTPException(status_code=400,detail = "Item already exists")
    else:
        db.add(new_tweet)
        db.commit()
        return new_tweet
        
    

@app.put('/tweet/{id}')
def update_tweet(id:int,likes:int) -> models.Tweet:
    tweet_fetched = db.query(models.Tweet).filter(id == models.Tweet.id).first()
    if tweet_fetched is None:
        raise HTTPException(status_code=404,detail = "Tweet not found!")
    else:
        tweet_fetched.likes = likes
        db.commit()
        return tweet_fetched

@app.delete('/tweet/{id}',status_code=status.HTTP_200_OK)
def delete_tweet(id:int) -> models.Tweet:
    tweet_fetched = db.query(models.Tweet).filter(id == models.Tweet.id).first()
    if tweet_fetched is None:
        return HTTPException(status_code=404,detail = "Tweet not found")
    else:
        db.delete(tweet_fetched)
        db.commit()
        return tweet_fetched

