import json

class Movie():
    
    def __init__(self, data):
        
        processed_data = json.loads(data)

        self.item_id = processed_data['ItemId']
        self.year = int(processed_data['Year'][:4])
        self.genre = processed_data['Genre'].replace(" ", "").split(",")
        
        if processed_data['imdbRating'] == 'N/A':
            self.imdb_rating = 6.3
        else:
            self.imdb_rating = float(processed_data['imdbRating'])
            
        if processed_data['imdbVotes'] == 'N/A':
            self.imdb_votes = 1
        else:
            self.imdb_votes = int(processed_data['imdbVotes'].replace(",", ""))
            
        
    def get_item_id(self):        
        return self.item_id