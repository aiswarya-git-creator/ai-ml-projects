# This is a Movie Recommendation System built with Python, Streamlit, Pandas, and Scikit-learn. It supports two types of recommendations:
* Collaborative Filtering: Based on user ratings.
* Content-Based Filtering: Based on movie genres.

# Collaborative Filtering
* Creates a user-movie rating matrix.
* Computes cosine similarity between users.
* Recommends movies liked by users similar to the selected user ID.

# Content-Based Filtering
* Uses genre flags to compute genre similarity.
* Matches input movie with similar genre profiles.
* Recommends the most similar movies.

# Dataset
* u.data: Contains user ratings.
* u.item: Contains movie titles and genre flags.
