import omdb
import pymongo
from keys import *

# mongo connection
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["Data_Assignment_3"]
my_collection = my_db["MovieData"]

# init
client = omdb.OMDBClient(apikey=movie_key)

search_keywords = ['Canada','University','Moncton','Halifax','Toronto','Vancouver''Alberta','Niagara']
# Reference taken from http://www.omdbapi.com/
for search_word in search_keywords:
    # Can iterate to 100 pages
    for pageCount in range(1, 95):
        # API call
        movies = client.search(search_word, page=pageCount)
        if movies == []:
            continue
        else:
            pass
        # inserting in mongo DB
        my_collection.insert_many(movies)