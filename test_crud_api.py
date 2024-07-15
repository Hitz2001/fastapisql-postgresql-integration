SQLALCHEMY_SILENCE_UBER_WARNING=1
def test_root(test_client):
    response = test_client.get("/")
    print(response.json(),"respose recieved")
    assert response.status_code == 200
    assert response.json() == {"message":"Hello world!"}
    
def test_tweet_upload(test_client,generate_tweet_json):
    response = test_client.post('/tweet',json=generate_tweet_json);
    assert response.status_code == 201
    assert response.json() == generate_tweet_json
    
def test_get_specific_tweet(test_client):
    response = test_client.get("/tweet/100");
    assert response.status_code == 404
    
    
def test_get_tweets(test_client):
    response = test_client.get('/tweets');
    assert response.status_code == 200