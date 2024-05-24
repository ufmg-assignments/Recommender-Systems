import numpy as np
from SGD import SGD

class Score():
    
    def __init__(self, user, movies_100,movies, sgd:SGD):
        
        self.user = user
        self.user_movies = list(user.movies.keys())
        self.user_ratings = np.array(list(user.movies.values()))
        self.num_movies_rated = len(self.user_ratings)
        self.target_movies = movies_100
        self.scores = np.zeros(100)
        self.movies = movies

        self.sgd_Results = sgd
        
        self.movies_model = self.target_movies + self.user_movies
    
    def cosine_similarity(self, u_vector, i_vector):

        user_norm = np.linalg.norm(u_vector) 
        item_norm = np.linalg.norm(i_vector)

        if user_norm == 0 or item_norm == 0:
            return 0
        return np.dot(u_vector, i_vector) / (user_norm * item_norm)
        
    def genre_score(self):
        
        categories = []
        for movie in self.movies_model:
            categories += self.movies[movie].genre
            
        categories = list(set(categories))
        
        if "N/A" in categories:
            categories.remove("N/A")
        
        movies_encoded = []
        
        for movie in self.movies_model:
            data = self.movies[movie].genre
            
            if "N/A" in data:
                data.remove("N/A")

            one_hot_encoded = [1 if category in data else 0 for category in categories]
            movies_encoded.append(one_hot_encoded)
            
            
        movies_watched_by_genre = np.sum(movies_encoded[100:], axis = 0)
        user_vector = self.user_ratings.dot(movies_encoded[100:])/10
        
        for i in range(len(user_vector)):
            if movies_watched_by_genre[i] != 0:
                user_vector[i] /= movies_watched_by_genre[i]
        
        ratings = np.array([self.movies[movie].imdb_rating for movie in self.target_movies])
        movies_vectors = movies_encoded[:100] * (ratings[:, np.newaxis]/10)
        
        genre_scores = np.zeros(100)
        cosine = np.zeros(100)
        euclidean = np.zeros(100)
        
        for i in range(100):
            movie_categories = self.movies[self.target_movies[i]].genre
            
            indexes = [index for index, genre in enumerate(categories) if genre in movie_categories]
            
            cosine[i] = self.cosine_similarity(user_vector, movies_vectors[i])
            euclidean[i] = np.linalg.norm(user_vector[indexes] - movies_vectors[i][indexes])
            
        euclidean = (euclidean - np.min(euclidean))/(np.max(euclidean) - np.min(euclidean))
        genre_scores = cosine + (1-euclidean)
        
        return genre_scores
    
    def imdb_score(self):
        
        imdb_scores = np.zeros(100)
        
        for i in range(100):
            imdb_scores[i] = self.movies[self.target_movies[i]].imdb_rating
    
        return imdb_scores
    
    def imdb_votes_score(self):
        
        imdb_votes_scores = np.zeros(100)
        
        for i in range(100):
            imdb_votes_scores[i] = self.movies[self.target_movies[i]].imdb_votes
    
        return imdb_votes_scores/np.max(imdb_votes_scores)
    
    def colaborative_score(self):
        
        colaborative_scores = np.zeros(100)
        
        target_user = self.user.user_id
        
        for i in range(100):

            target_movie = self.target_movies[i]
            
            try:
                prediction = self.sgd_Results.prediction(self.sgd_Results.P, self.sgd_Results.Q , target_user, target_movie)

            except:
                prediction = 6.3

            colaborative_scores[i] = prediction
            
        return colaborative_scores

    def calculate_final_score(self):
        
        self.scores = self.imdb_score() + 5 * self.imdb_votes_score() + \
                      10*self.imdb_votes_score()*self.imdb_score() + 0.2*self.colaborative_score() + \
                      0.5*self.genre_score()
    
    def get_rank(self):

        indexes_top_100 = np.argsort(self.scores)[::-1]
        
        top_100_items = [self.target_movies[i] for i in indexes_top_100]
        
        return top_100_items