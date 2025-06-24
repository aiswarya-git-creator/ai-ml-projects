# movie_recommendation_app.py

import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# Load datasets
def load_data():
    ratings = pd.read_csv("data/u.data", sep='\t', names=["user_id", "movie_id", "rating", "timestamp"])
    movies = pd.read_csv("data/u.item", sep='|', encoding='latin-1',
                         names=["movie_id", "title", "release_date", "video_release_date", "IMDb_URL",
                                "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
                                "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
                                "Romance", "Sci-Fi", "Thriller", "War", "Western"])
    data = pd.merge(ratings, movies[["movie_id", "title"]], on="movie_id")
    return data, movies

# Collaborative Filtering
def build_user_movie_matrix(data):
    user_movie_matrix = data.pivot_table(index='user_id', columns='title', values='rating')
    user_movie_matrix.fillna(0, inplace=True)
    return user_movie_matrix

def collaborative_recommendations(user_id, similarity, data, num_recommendations=5):
    if user_id < 1 or user_id > 943:
        return ["Invalid User ID"]
    similar_users = list(enumerate(similarity[user_id - 1]))
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[1:]
    top_users = [user[0] + 1 for user in similar_users[:5]]
    recommended_movies = data[data['user_id'].isin(top_users)]['title'].value_counts().head(num_recommendations)
    return recommended_movies.index.tolist()

# Content-Based Filtering
def build_genre_matrix(movies):
    genre_columns = ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama",
                     "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller",
                     "War", "Western"]
    movie_genres = movies.set_index("title")[genre_columns]
    return movie_genres

def content_based_recommend(movie_name, movie_genres, num=5):
    movie_name = movie_name.strip()
    all_titles = [title.lower() for title in movie_genres.index]

    matches = get_close_matches(movie_name, all_titles, n=1, cutoff=0.6)
    if not matches:
        return ["Movie not found in database"]

    matched_title = matches[0]
    matched_index = all_titles.index(matched_title)
    genre_similarity = cosine_similarity(movie_genres)
    sim_scores = list(enumerate(genre_similarity[matched_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num + 1]
    return [movie_genres.index[i[0]] for i in sim_scores]

# Streamlit UI
# Streamlit UI
st.set_page_config(page_title="Movie Recommendation System", layout="centered", page_icon="🎬")
st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

option = st.radio("Select Recommendation Type", ("Collaborative", "Content-Based"))
data, movies = load_data()
movie_titles = sorted(movies["title"].unique())  # 🟢 This line should be here globally

if option == "Collaborative":
    user_id = st.number_input("Enter User ID (1-943):", min_value=1, max_value=943, step=1)
    if st.button("Recommend"):
        st.subheader("Recommended Movies:")
        matrix = build_user_movie_matrix(data)
        similarity = cosine_similarity(matrix)
        recs = collaborative_recommendations(user_id, similarity, data)
        for movie in recs:
            st.write(movie)

else:
    movie_name = st.selectbox("Select a Movie Title:", movie_titles)
    if st.button("Recommend"):
        movie_genres = build_genre_matrix(movies)
        recs = content_based_recommend(movie_name, movie_genres)
        st.subheader("Movies you might like:")
        for movie in recs:
            st.write(movie)
