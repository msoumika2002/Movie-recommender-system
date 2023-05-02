import streamlit as st
import pickle
import pandas as pd
import requests
import zipfile
st.set_page_config(layout="wide")
backgroundColor = '#273346'
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e4bf05014f94b5f0b973d4d2a8bbf48c&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']

with zipfile.ZipFile('similarity.zip', 'r') as zip_ref:
    zip_ref.extract('similarity.pkl')

def recommend(movie):
    m_index = movies[movies['title'] == movie].index[0]
    distances = similarity[m_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    recommended_movies_match=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_match.append(i[1])
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters,recommended_movies_match

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values)

if st.button('Recommend'):

    st.write('The top 5 movies similar to',"'",selected_movie_name,"'",'are:')
    names,posters,match=recommend(selected_movie_name)
    col1, col2, col3,col4,col5= st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.write('Match:',round(match[0] * 100,2),'%')
    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.write('Match:', round(match[1] * 100, 2), '%')
    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.write('Match:', round(match[2] * 100, 2), '%')
    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.write('Match:', round(match[3] * 100, 2), '%')
    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.write('Match:', round(match[4] * 100, 2), '%')

