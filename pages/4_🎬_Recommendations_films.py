import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from PIL import Image
from io import BytesIO
import requests
import time
import spacy
#from st_click_detector import click_detector
import timeit
#import concurrent.futures
from deep_translator import GoogleTranslator
import urllib.request 
import spacy_streamlit
st.set_page_config(
    page_title="Recommandation de films",
    page_icon="🎬",
    layout="wide",
)

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #980321;
    color:#FFFFFF;
}
div.stButton > button:hover {
    background-color: #FFFFFF;
    color:#000000;
    }
</style>""", unsafe_allow_html=True)

# sidebar

st.markdown(
    """
<style>
.css-nzvw1x {
    background-color: #061E42 !important;
    background-image: none !important;
}
.css-1aw8i8e {
    background-image: none !important;
    color: #FFFFFF !important
}
.css-ecnl2d {
    background-color: #496C9F !important;
    color: #496C9F !important
}
.css-15zws4i {
    background-color: #496C9F !important;
    color: #FFFFFF !important
}
</style>
""",
    unsafe_allow_html=True
)

st.title('Moteur de recommandation de films')
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NGU4YzQ0MTRiNzA4ZWQwMGNkMDJjYzk1MzFiOTA1MCIsInN1YiI6IjY1NTM4ZTNlZDRmZTA0MDBmZTA1NDRhMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JswePi_MXWCPSxorJVXpZFPdz0zWVXCu15m2TgE5q4o"
}
# Initialize session state
if 'show_description' not in st.session_state:
    st.session_state.show_description = False
    
# Load English tokenizer, tagger, parser and NER

@st.cache_data
def load_data():
    nlp = spacy.load("en_core_web_sm")
    df = pd.read_parquet('df_french_2.parquet.gzip')
    X = pd.read_parquet('Xbiais.parquet.gzip')
    return(nlp, df , X)
nlp, df, X = load_data()

# We train the model
@st.cache_resource
def train_model():
    distanceNN = NearestNeighbors(n_neighbors=6)
    distanceNN.fit(X)
    return(distanceNN)
#We create a selector where the user can enter a movie name
movie_name = st.selectbox("Choisissez un film pour lequel vous souhaitez des recommandations :", df.primaryTitle, None)

try:

    # we retrieve the full dataframe for the row with the selected movie
    movie_name = df[df.primaryTitle.str.contains(movie_name)].index[0]
    # we do a regression for the movie
    distanceNN = train_model()
    nearest_movies = distanceNN.kneighbors(X.loc[X.index == movie_name],return_distance=False)
except:
    st.write("Aucun film n'a été selectionné")

resizedImages = []
movies = []
movies_names = []
movie_overview = []
movie_genre = []
release_date = []
movie_video = []
movie_trailer = []
# Here we append the relevant information to lists
try:
    for index in df.primaryTitle.loc[X.iloc[nearest_movies[0]].index][1:]:
        movies.append(df.poster_path.loc[df.primaryTitle == index][0])
        movies_names.append(index)
        movie_overview.append(df.overview.loc[df.primaryTitle == index][0])
        movie_genre.append(df.genres.loc[df.primaryTitle == index][0])
        release_date.append(df.startYear.loc[df.primaryTitle == index][0])
        movie_video.append(int(df.API_id.loc[df.primaryTitle == index][0]))
        movie_trailer.append(df.trailer_key.loc[df.primaryTitle == index][0])
except:
    st.write("")
# We create 5 columns
col0, col1, col2, col3, col4 = st.columns(5)
colist = [col0, col1, col2, col3, col4]

if st.session_state.show_description == False:
    # This loop puts pictures and buttons inside columns
    for i, (movie, name, overview, genre, release_date, trailer) in enumerate(zip(movies, movies_names, movie_overview, movie_genre, release_date, movie_trailer)):
        with colist[i]:
            try:
                urllib.request.urlretrieve(f'https://image.tmdb.org/t/p/original/{movie}', "poster")
                image = Image.open("poster")
                new_image = image.resize((500, 750))
                st.image(new_image,use_column_width=True)
            except:
                st.image("poster.png")
            st.session_state.picked_movie = {'name': name, 'overview':overview, 'genre':genre, 'picture':movie, 'i':i, 'release_date':release_date, 'trailer':trailer}
            if st.button(name, key=i):
                st.session_state.show_description = True
                st.rerun()
else:
    col0, col1 = st.columns(2)
    with col0:
        try:
            st.image(f"https://image.tmdb.org/t/p/original/{movies[st.session_state.picked_movie['i']]}",width=600)
        except:
            st.write("")
    with col1:
        st.subheader(f"Titre : {st.session_state.picked_movie['name']}")
        st.subheader(f"Genre : {st.session_state.picked_movie['genre']}")
        st.subheader(GoogleTranslator(source='auto', target='fr').translate(f"Synopsis : {st.session_state.picked_movie['overview']}"))
        st.subheader(f"Année de sortie : {str(int(st.session_state.picked_movie['release_date']))}")
        if st.session_state.picked_movie['trailer'] != '0':
            st.video(f"https://youtu.be/{st.session_state.picked_movie['trailer']}")
    if st.button("Retour"):
        st.session_state.show_description = False
        st.rerun()
