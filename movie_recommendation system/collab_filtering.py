import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv('movies.csv')
ratings = pd.merge(movies,ratings).drop(['genres','timestamp'],axis=1)
#print(ratings.head())

user_ratings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')


#drop movies that have less than 10 users rating them
user_ratings = user_ratings.dropna(thresh=10,axis=1).fillna(0)
#print(user_ratings.head())

item_similarity_df = user_ratings.corr(method='pearson')
#print(item_similarity_df.head(50))


def get_similar(movie_name,rating):
    similar_ratings = item_similarity_df[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    #print(type(similar_ratings))
    return similar_ratings

action_lover = [("Amazing Spider-Man, The (2012)",5),("Mission: Impossible III (2006)",4),("Toy Story 3 (2010)",2),("2 Fast 2 Furious (Fast and the Furious 2, The) (2003)",4)]
similar_movies = pd.DataFrame()
for movie,rating in action_lover:
    similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)

similar_movies.head(10)
similar_movies.sum().sort_values(ascending=False).head(20)

print(similar_movies.head(10))