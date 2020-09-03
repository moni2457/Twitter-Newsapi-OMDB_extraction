import omdb
from keys import *
# init
client = omdb.OMDBClient(apikey=movie_key)

search_keywords = ['Canada','University','Moncton','Halifax','Toronto','Vancouver''Alberta','Niagara']
movie_title = []

# # Reference taken from http://www.omdbapi.com/
for search_word in search_keywords:
    # Can iterate to 100 pages but limited API calls per day
    for pageCount in range(1,2):
        movies = client.search(search_word, page=pageCount)
        if movies == []:
            continue
        else:
            movie_title.append(movies)
            pass

movie_details = []
# Reference taken from http://www.omdbapi.com/
for movie in movie_title:
    for obj in movie:
        # invoked get api call for every movie title
        movie_details.append(client.get(title=obj["title"]))
print(movie_details)
