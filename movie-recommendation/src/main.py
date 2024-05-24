import sys
import pandas as pd

from DatabaseHandler import DatabaseHandler
from SGD import SGD
from Score import Score

if __name__ == "__main__":

    # Storing file names from user's input:
    ratingsFilename = sys.argv[1]
    contentFilename =  sys.argv[2]
    targetsFilename = sys.argv[3]

    # Saving targets information in advance:
    targets = pd.read_csv(targetsFilename)
    # Reading and saving User's and Movie's data:
    database = DatabaseHandler(users_ratings=ratingsFilename, movies_content=contentFilename) 
    
    # Creating a dataframe with the user's ratings dictionary
    ratings = pd.DataFrame(data= database.ratings_list) 

    row_per_user = ratings['UserId'].unique()
    row_per_user = {value: index for index,value in enumerate(row_per_user)}     

    column_per_item = ratings['ItemId'].unique()
    column_per_item = {value: index for index,value in enumerate(column_per_item)}

    N = len(column_per_item)
    M = len(row_per_user)

    users_ratings = {}
    for index, row in ratings.iterrows():
        users_ratings[(row['UserId'],row['ItemId'])] = row["Rating"]

    # Implementing SGD method for prediction:
    sgd_method = SGD(row_user=row_per_user, column_item=column_per_item,M=M,N=N)
    users_latent_factor, itens_latent_factors = sgd_method.sgd(users_ratings,K = 10, alpha = 0.005, reg = 0.035, epoches = 10)

    # Scores:
    user_targets = targets.groupby('UserId')['ItemId'].agg(list).reset_index()

    print("UserId,ItemId")

    for index, row in user_targets.iterrows():
        
        user_id = row['UserId']
        item_ids = row['ItemId']

        score = Score(user=database.users[user_id],movies_100=item_ids,sgd=sgd_method,movies=database.movies)
        score.calculate_final_score()
        rank = score.get_rank()
        
        for movie in rank:
            print(user_id + "," + movie)



