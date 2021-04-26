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

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_weather():

    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    mentions = api.mentions_timeline(
                last_seen_id,
                tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + "-"+ mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

        if '#weather' in mention.full_text.lower():
            print('found the tweet')
            city_name = 'Chicago'
            try:
                # needs to be updated for user input

                api_address =  'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + secret_keys.OPEN_WEATHER_KEY
                json_data = requests.get(api_address).json()
                formatted_data = json_data['weather'][0]['description']
                api.update_status('@' + mention.user.screen_name + ' The weather is ' + formatted_data, mention.id)

            except tweepy.TweepError as error:
                print("I don't know that city, try again", error)
        else:
            print("You done messed up")
            #api.update_status('@' + mention.user.screen_name + ' I need a #hike to find the city', mention.id)

while True:
    reply_weather()
    time.sleep(15)




































