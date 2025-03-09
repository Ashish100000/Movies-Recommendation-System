import streamlit as st
import pickle
import pandas as pd
import requests
import time


# Function to fetch movie posters
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=eeef4327fb4a807ab483a135342f8b1d&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500"  # Fallback placeholder


# Function to get movie recommendations
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load data
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Custom Styles
st.markdown(
    """
    <style>
    body {background-color: #121212; color: white;}
    .movie-title {font-size: 16px; font-weight: bold; text-align: center; margin-top: 10px;}
    .recommend-button {background-color: #ff5733; color: white; font-size: 20px; border-radius: 10px; width: 200px; text-align: center;}
    .loader {text-align: center; font-size: 20px; margin-top: 20px;}
    </style>
    """,
    unsafe_allow_html=True
)

# UI Design
st.markdown("<h1 style='text-align: center; color: #FF5733;'>🍿 Movie Recommendation System 🎬</h1>",
            unsafe_allow_html=True)
selected_movie_name = st.selectbox("🎥 **Select a Movie:**", movies['title'].values)

# Recommend button with animation
if st.button("🔥 Recommend", key="recommend_button"):
    with st.spinner("⏳ Finding the best movies for you..."):
        time.sleep(2)  # Simulating loading animation
        names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.image(poster, use_container_width=True)
                st.markdown(f"<p class='movie-title'>{name}</p>", unsafe_allow_html=True)
    else:
        st.write("⚠️ No recommendations found. Try selecting another movie.")
