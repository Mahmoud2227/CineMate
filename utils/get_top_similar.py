import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity 

def get_top_similar(ratings_df, movies_df, movieid=1, topn=5):
    ratings = ratings_df.copy()
    movies = movies_df.copy()
    movie_data = pd.merge(ratings, movies, on='movieId')
    year_extracted = movies["title"].str.extract(r'((\d{4}))')
    movies["year"] = year_extracted[0]
    movies["year"].fillna(1995, inplace=True)
    movies["year_cat"]=pd.cut(movies["year"].astype(int), bins=[1900, 1970, 1990, 2000, 2010, 2020], labels=["1900-1970", "1970-1990", "1990-2000", "2000-2010", "2010-2020"])
    year_cat=pd.get_dummies(movies["year_cat"],dtype=int)
    year_cat["movieId"]=movies["movieId"]
    movie_genres = movies.set_index('movieId')['genres'].str.get_dummies(sep='|')
    utility_matrix= movie_data.pivot_table(index='movieId', columns='userId', values='rating')
    utility_matrix.fillna(0, inplace=True)
    final=utility_matrix.merge(movie_genres, on='movieId', how='inner')
    final=final.merge(year_cat, on='movieId', how='inner')
    final.set_index('movieId', inplace=True)
    similarity=cosine_similarity(final)
    similarity=pd.DataFrame(similarity, index=final.index, columns=final.index,dtype=float)

    index1=similarity[movieid].sort_values(ascending=False).index[1:topn+1]
    val=val=similarity[movieid].sort_values(ascending=False).values[1:topn+1]
    df=pd.DataFrame(val,index=index1).rename(columns={0:"similarity"}).set_index(index1)
    return df.merge(movies.set_index("movieId"), on='movieId')