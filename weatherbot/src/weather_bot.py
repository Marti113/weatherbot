import tweepy
import requests
import time

from os import environ
try:
    import secret_keys
except ImportError:
    pass

print("This is my weather bot")

if 'CONSUMER_KEY' in environ:
    CONSUMER_KEY = environ['CONSUMER_KEY']
    CONSUMER_SECRET= environ['CONSUMER_SECRET']
    ACCESS_KEY= environ['ACCESS_KEY']
    ACCESS_SECRET= environ['ACCESS_SECRET']
else:
    CONSUMER_KEY = secret_keys.CONSUMER_KEY
    CONSUMER_SECRET = secret_keys.CONSUMER_SECRET
    ACCESS_KEY = secret_keys.ACCESS_KEY
    ACCESS_SECRET = secret_keys.ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def capture_user_city():

    mentions = api.mentions_timeline(
    tweet_mode='extended'
    )

    for mention in reversed(mentions):
        if '#hike' in mention.full_text.lower():
            city_name = mention.full_text.split('#hike')
            # needs to be updated for user input
            #city_name = 'Asheville'
            api_address = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=62c7ceaaad980045d006ea4704872c79'

            json_data = requests.get(api_address).json()
            formatted_data = json_data['weather'][0]['description']
            print(formatted_data)
            try:
                api.update_status('@' + mention.user.screen_name + ' The weather is '+ formatted_data, mention.id)
            except tweepy.TweepError as error:
                print("I don't know that city, try again", error)
        else:
            api.update_status('@' + mention.user.screen_name + ' I need a #hike to find the city', mention.id)

while True:
    capture_user_city()
    time.sleep(15)