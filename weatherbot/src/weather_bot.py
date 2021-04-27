import tweepy
import requests
import time
import argparse

from os import environ

from name_search import NameSearch

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
    OPEN_WEATHER_KEY = environ['OPEN_WEATHER_KEY']
else:
    CONSUMER_KEY = secret_keys.CONSUMER_KEY
    CONSUMER_SECRET = secret_keys.CONSUMER_SECRET
    ACCESS_KEY = secret_keys.ACCESS_KEY
    ACCESS_SECRET = secret_keys.ACCESS_SECRET
    OPEN_WEATHER_KEY = secret_keys.OPEN_WEATHER_KEY

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

def reply_tweet(full_text, id, user_screen_name):
    print(str(id) + "-" + full_text)

    if '#weather' in full_text.lower():
        print('found the tweet')
        city = NameSearch(full_text)
        city_link = city.find_place()
        city_name = city.return_city()
        try:

            api_address = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_link + OPEN_WEATHER_KEY
            json_data = requests.get(api_address).json()
            formatted_data = json_data['weather'][0]['description']
            status_update = '@' + user_screen_name + ' The weather in '+ city_name +' is ' + formatted_data
            return status_update
        except tweepy.TweepError as error:
            print("I don't know that city, try again", error)
    else:
        print("No #weather in text")

    return None

def reply_weather():
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    mentions = api.mentions_timeline(
               last_seen_id,
              tweet_mode='extended')

    for mention in reversed(mentions):
        full_text, id, user_screen_name = mention.full_text, mention.id, mention.user.screen_name
        reply_result = reply_tweet(full_text, id, user_screen_name)
        if reply_result is not None:
            api.update_status(reply_result, id)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

parser = argparse.ArgumentParser(description='Twitter weather bot')
parser.add_argument('--test', action='store_true')
args = parser.parse_args()
print("In test mode:", args.test)

if not args.test:
    while True:
       reply_weather()
       time.sleep(15)
else:
    result = reply_tweet("This is a test #weather tweet for Fort Lauderdale", 0, 'test_name')
    print(result)



