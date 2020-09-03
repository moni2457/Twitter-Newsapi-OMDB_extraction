import tweepy as tw
from keys import *
from cleaning_script import *
import pymongo

# keys are defined here
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# mongodb connection
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["Data_Assignment_3"]
my_collection = my_db["twitter_search"]

# search keywords array
search_keywords = ['Canada', 'University', 'Dalhousie University', 'Halifax', 'Canada Education']

# tweet_details list -  array
tweets_list = []
tweet_metadata = {}
# search API for twitter using tweepy
# Reference for extraction of twitter process through search api taken from https://www.earthdatascience.org/courses/earth-analytics-python/using-apis-natural-language-processing-twitter/get-and-use-twitter-data-in-python/

for search_word in search_keywords:
    get_tweets = tw.Cursor(api.search,
                           q=search_word,
                           tweet_mode='extended'
                           ).items(700)
    file = open("data_file.txt","a+")        # creating a new text file
    for tweet in get_tweets:        # creating the metadata of tweets
        # fetching as well as cleaning the tweets
        text = clean_emoticons(tweet.full_text)
        text = clean_special_characters(text)
        tweet_metadata['text'] = clean_URL(text)
        if tweet_metadata['text']:
            file.write(tweet_metadata['text'])
        name = clean_emoticons(tweet.user.name)
        name = clean_special_characters(name)
        tweet_metadata['name'] = clean_URL(name)
        user_name = clean_emoticons(tweet.user.screen_name)
        user_name = clean_special_characters(user_name)
        tweet_metadata['user_name'] = clean_URL(user_name)
        tweet_metadata['account_creation_date'] = tweet.created_at.strftime("%b-%d-%Y")
        tweet_metadata['account_verification_status'] = tweet.user.verified
        location = clean_emoticons(tweet.user.location)
        tweet_metadata['location'] = clean_special_characters(location)
        tweet_metadata = {                          # creating the meta data
            "text": tweet_metadata['text'],
            "name": tweet_metadata['name'],
            "user_name": tweet_metadata['user_name'],
            "account_creation_date": tweet_metadata['account_creation_date'],
            "account_verification_status": tweet_metadata['account_verification_status'],
            "location": tweet_metadata['location']
        }
        tweets_list.append(tweet_metadata)

my_collection.insert_many(tweets_list) # inserting data in the mongoDB
file.close() # closing the text file
print("Completed")
