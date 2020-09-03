from newsapi import NewsApiClient
import pymongo
from cleaning_script import *
from keys import *

# Init
newsapi = NewsApiClient(api_key=news_key)

# mongo DB connection
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["Data_Assignment_3"]
my_collection = my_db["NewsApi"]

latest_news_arr = []
news_obj = {}

search_keywords = ['Canada', 'University', 'Dalhousie University', 'Halifax', 'Canada  Education', 'Moncton', 'Toronto']
# Reference of API call from https://newsapi.org/
for search_word in search_keywords:
    # api call
    all_articles = newsapi.get_everything(q=search_word, page_size=100)
    file = open("data_file.txt", "a+") # creating a file
    for article in all_articles['articles']:    # extracting and cleaning articles
        news_obj['description'] = clean_special_tags(article['description'])
        if news_obj['description']:         # writing articles in file
            file.write(news_obj['description'])
        news_obj['author'] = clean_special_tags(article['author'])
        news_obj['publishedAt'] = article['publishedAt']
        news_obj['title'] = clean_special_tags(article['title'])
        news_obj['url'] = article['url']
    # creating the object
        news_obj = {
            "description": news_obj['description'],
            "author": news_obj['author'],
            "title": news_obj['title'],
            "publishedAt": news_obj['publishedAt'],
            "url": news_obj['url']
        }
        latest_news_arr.append(news_obj)

# inserting articles in mongo DB
my_collection.insert_many(latest_news_arr)
file.close() # close file
print("Completed")

