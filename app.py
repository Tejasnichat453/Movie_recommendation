import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.parse

# Function to get movie poster URL
def poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=6edfed7250aa64fe872ca1cd1cd07f48".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Set page config
st.set_page_config(
    page_title="Movie Recommendation",  # Removed spaces around the title
    page_icon=":clapper:",
    layout="wide"
)

# Add background animation and font styling
st.markdown(
    """
    <style>
        body {
            background-image: url("https://your-animation-url.gif");  /* Replace with your animation URL */
            background-size: cover;
            background-repeat: no-repeat;
            font-family: 'Arial', sans-serif;
        }
        /* ... (rest of your styling remains the same) */
    </style>
    """,
    unsafe_allow_html=True
)

# Animated title with emoji
st.markdown("""
<h1 style="text-align: center; animation: pulsate 1s infinite;"> MOVIES RECOMMENDATION </h1>
""", unsafe_allow_html=True)

# Main content

st.markdown("<h1 style='text-align: center; background-color:rgb(0, 191, 255); padding: 10px;'>YOUR CHOICES</h1>", unsafe_allow_html=True)

# Load movie data and similarity matrix
movies_df = pickle.load(open('movie.pkl', 'rb'))
movies = pd.DataFrame(movies_df)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection and recommendation
option = st.selectbox('TYPE YOUR MOVIE NAME?', movies["title"].values)

# Use st.markdown with markdown=True to apply custom styling to the selectbox options
st.markdown("""
    <style>
        /* Add your CSS styling here */
        select {
            color: blue;
            font-size: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Display the selected option
st.write(f"You selected: {option}")




if st.button('Recommend', key='recommend_button'):
    recommended_movies, movie_posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(recommended_movies[0])
        st.image(movie_posters[0], caption=recommended_movies[0], use_column_width=True)

    with col2:
        st.header(recommended_movies[1])
        st.image(movie_posters[1], caption=recommended_movies[1], use_column_width=True)

    with col3:
        st.header(recommended_movies[2])
        st.image(movie_posters[2], caption=recommended_movies[2], use_column_width=True)

    with col4:
        st.header(recommended_movies[3])
        st.image(movie_posters[3], caption=recommended_movies[3], use_column_width=True)

    with col5:
        st.header(recommended_movies[4])
        st.image(movie_posters[4], caption=recommended_movies[4], use_column_width=True)

# Search bar for YouTube trailer search
with st.container():
    st.subheader("Search for Movie Trailers on YouTube")
    search_query = st.text_input(" Enter a movie title", "", key='youtube_search')
    search_button = st.button("Search ", key='search_button')

# Only display the search results if the button is clicked and a query is entered
if search_button and search_query:
    encoded_search_query = urllib.parse.quote(search_query)
    search_link = f"https://www.youtube.com/results?search_query={encoded_search_query}+trailer"

    # Use a prominent heading for the results
    st.header(f"Search Results for '{search_query}' Trailer on YouTube")

    # Display the link as a visually appealing button
    st.markdown(f'<a href="{search_link}" target="_blank"><button>Click here to watch on YouTube</button></a>',
                unsafe_allow_html=True)