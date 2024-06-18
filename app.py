import streamlit as st
import pickle
import pandas as pd
import requests
movies_dict = pickle.load(open("movie_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl","rb"))


def fetch_poster(title):
    #response = requests.get("https://api.themoviedb.org/3/movie/{"
                            #"}?""api_key=8265db1679663a7ea12ac168da84d2e8&language=en-US", format(movie_id))
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey=cef6adb")
    data = response.json()
    poster_url = data["Poster"]
    poster_content = requests.get(poster_url).content
    return poster_content


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_title))
    return recommend_movies,recommended_movies_poster


st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Select the movies",movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col5:
        st.text(names[0])
        st.image(posters[0])

    with col1:
        st.text(names[1])
        st.image(posters[1])

    with col2:
        st.text(names[2])
        st.image(posters[2])

    with col3:
        st.text(names[3])
        st.image(posters[3])

    with col4:
        st.text(names[4])
        st.image(posters[4])


