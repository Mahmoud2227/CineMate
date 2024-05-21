import numpy as np


def predict_top_n_with_loaded_model(loaded_model, ratings, movies, user_id, n=10):
    user_ids = ratings["userId"].unique().tolist()
    movie_ids = ratings["movieId"].unique().tolist()

    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}

    movie_encoded2movie = {i: x for x, i in movie2movie_encoded.items()}

    ratings["user"] = ratings["userId"].map(user2user_encoded)
    ratings["movie"] = ratings["movieId"].map(movie2movie_encoded)

    all_genres = set()
    for genres in movies["genres"].str.split("|"):
        all_genres.update(genres)
    all_genres = sorted(all_genres)

    genre2genre_encoded = {x: i for i, x in enumerate(all_genres)}

    def encode_genres(genres):
        encoded = np.zeros(len(all_genres))
        for genre in genres.split("|"):
            if genre in genre2genre_encoded:
                encoded[genre2genre_encoded[genre]] = 1
        return encoded

    movies["genre_encoded"] = movies["genres"].apply(encode_genres)

    ratings = ratings.merge(
        movies[["movieId", "genre_encoded"]], on="movieId", how="left"
    )

    ratings = ratings.sort_values(["userId", "timestamp"])

    user_encoded = user2user_encoded[user_id]
    movie_ids = movies["movieId"].values

    valid_movie_ids = [
        movie_id for movie_id in movie_ids if movie_id in movie2movie_encoded
    ]
    valid_movie_encoded = [
        movie2movie_encoded[movie_id] for movie_id in valid_movie_ids
    ]
    genre_encoded = np.stack(
        movies[movies["movieId"].isin(valid_movie_ids)]["genre_encoded"].values
    )

    user_array = np.array([user_encoded] * len(valid_movie_encoded))

    predictions = loaded_model.predict(
        [user_array, np.array(valid_movie_encoded), genre_encoded]
    )
    predictions = predictions.flatten()

    top_n_indices = predictions.argsort()[-n:][::-1]
    top_n_movie_ids = [
        movie_encoded2movie[valid_movie_encoded[i]] for i in top_n_indices
    ]

    return top_n_movie_ids
