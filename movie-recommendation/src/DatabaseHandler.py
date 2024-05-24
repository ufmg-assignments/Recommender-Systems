import json

from Movie import Movie
from User import User

class DatabaseHandler():
    def __init__(self, users_ratings, movies_content):

         # Getting Movies information:
        movies = {}
        moviesFile = open(movies_content, "r")

        for line in moviesFile.readlines():

            movie = Movie(line)
            item_id = movie.get_item_id()
            
            movies[item_id] = movie
            
        moviesFile.close()
        del moviesFile # Cleans memory

        # Getting Users information:
        users = {}
        ratingsFile = open(users_ratings, "r")

        for line in ratingsFile.readlines():

            processed_data = json.loads(line)
            
            user_id = processed_data["UserId"]
            item_id = processed_data["ItemId"]
            rating = processed_data["Rating"]
            
            if user_id in users:
                users[user_id].add_movie(item_id, rating)
            else:
                users[user_id] = User(user_id, item_id, rating)
            
        ratingsFile.close()

        # Handling ratings and attaching to the users:
        ratings_list= []
        with open(users_ratings, 'r') as file:
            for line in file:
                ratings_list.append(json.loads(line))

        self.users = users
        self.movies = movies
        self.ratings_list = ratings_list

        def get_users(self):
            return self.users
        
        def get_movies(self):
            return self.movies