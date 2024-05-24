class User():
    
    def __init__(self, user_id, item_id, rating):
        
        self.user_id = user_id
        self.movies = {item_id: int(rating)}
        
    def get_user_id(self):
        
        return self.user_id
    
    def add_movie(self, movie, rating):
        
        self.movies[movie] = rating
        