import tweepy as tw
from keys import *
from cleaning_script import *
import pymongo

# keys are defined here
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

# mongodb connection
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["Data_Assignment_3"]
my_collection = my_db["twitter_stream"]
# file open
file = open("data_file.txt", "a+")

# Reference taken from https://stackoverflow.com/questions/20863486/tweepy-streaming-stop-collecting-tweets-at-x-amount

class StdOutListener(tw.StreamListener):

    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0

    def on_status(self, status):
        # fetching and cleaning tweets
        tweet = clean_emoticons(status.text)
        tweet = clean_special_characters(tweet)
        tweet = clean_URL(tweet)
        if tweet is not None: # writing tweets in file
            file.write(tweet)
        name = clean_emoticons(status.user.name)
        name = clean_special_characters(name)
        name = clean_URL(name)
        user_name = clean_emoticons(status.user.screen_name)
        user_name = clean_special_characters(user_name)
        user_name = clean_URL(user_name)
        location = clean_emoticons(status.user.location)
        location = clean_special_characters(location)
        account_creation_date = status.created_at.strftime("%b-%d-%Y")
        # creating the metadata
        record = {'Tweet': tweet, 'Created At': account_creation_date, 'Name': name, 'Location': location,
                  'User_name': user_name}
        self.num_tweets += 1
        # setting limit for streaming upto 3500
        if self.num_tweets < 3500:
            my_collection.insert(record)
            return True
        else:
            return False

    def on_error(self, status):
        print 'Error', status

    def on_limit(self, status):
        print 'Limit exceeded', status

    def on_timeout(self, status):
        print 'Stream disconnected'


stream = tw.Stream(auth, StdOutListener())
stream.filter(track=['Canada', 'University', 'Dalhousie University', 'Halifax', 'Canada Education'])
file.close() # file close
print("Completed")
