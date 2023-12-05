# IMPORTS
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import Image
from io import BytesIO
import requests
import time
#from sklearn.neighbors import NearestNeighbors

import plotly.io as pio
pio.templates.default = "none"

st.set_page_config(
    page_title="Dashboard Projet 2",
    page_icon="📈",
    layout="wide",
)

# CONFIGURATION GENERALE

# CHARGEMENT DES DATAFRAMES
df_final = pd.read_parquet('df_final.parquet.gzip')
#df_final_2 = pd.read_parquet('df_final_2.parquet.gzip')
df_french = pd.read_parquet('df_french.parquet.gzip')
meanage = pd.read_parquet('actors_mean_age.parquet.gzip')
moviesbydecades = pd.read_parquet('moviesbydecades.parquet.gzip')
movies = pd.read_parquet('movies.parquet.gzip')
notepargenre = pd.read_parquet('note_par_genre.parquet.gzip')
nombrepargenre = pd.read_parquet('nombrepargenre.parquet.gzip')
df2 = pd.read_parquet('df2.parquet.gzip')
# MODIFS SUR LES DATAFRAMES
df_genres = df_final.copy()
df_genres['genre'] = df_genres['genres'].apply(lambda x: x.split(",")[0] if pd.notnull(x) else x)
df_genres['decade'] = df_genres['startYear'].apply(lambda x: (x//10)*10)

# CODE STREAMLIT
#st.title('KPIs Cinema')  
st.markdown("<h1 style='text-align: center; color: white;'>Quelques graphiques sur l'ensemble des données IMDB et TMDB</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>---</h2>", unsafe_allow_html=True)

# CODE DES GRAPHIQUES

#graph_runtime = px.scatter(df_final_2, x='startYear',y='runtimeMinutes',title="Scatterplot des durees de films",hover_name="primaryTitle", hover_data="runtimeMinutes", color='titleType')


graph_movies_decade = px.line(moviesbydecades,x=moviesbydecades.index,y=moviesbydecades.runtimeMinutes, title = "Durée moyenne des films par décennie", labels={'decades':'décennies','runtimeMinutes':'durée des films'},color_discrete_sequence =['#980321'])

graph_age_moyen = px.line(meanage,x=meanage.index,y=meanage.age, title = "Âge moyen des acteurs/actrices par décennie", labels={'age':'âge','decades':'décennies'},color_discrete_sequence =['#980321'])
#df = df_genres.genre.value_counts().reset_index()
graph_genres = px.bar(df2,x='genre',y='count',labels={'genre':'genre','count':'compte'}, title = "Nombre de films par genre")
#st.dataframe(df_genres.genre.value_counts().reset_index())
graph_repartition_votes = px.histogram(movies, x=movies.numVotes.loc[movies.numVotes < 400], title = "Répartition des films par nombre de votes")

graph_genre_acteuresses = px.bar(nombrepargenre, 'decades', 'genre',color='primaryProfession',barmode="group", title = "Répartition par décennie et par sexe", labels={'genre':'compte','decades':'décennies'})

fig = make_subplots(rows=2, cols=2,subplot_titles=(" titre du premier graphique", "Répartition des films par genre", "Age moyen des acteurs/actrices par décennie","Durée moyenne des films par décennie"))

fig1 = graph_genres
fig2 = graph_age_moyen
fig3 = graph_movies_decade
fig4 = graph_genre_acteuresses
fig3.update_traces(line_color="#FF7F0E")
fig2.update_traces(line_color="#FF7F0E")
fig2.update_traces(line=dict(width=3))
fig3.update_traces(line=dict(width=3))
newnames = {'actor':'acteurs', 'actress': 'actrices'}
fig4.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
fig4.update_layout(legend_title_text='Répartition')
fig1.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
fig2.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
fig3.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
fig4.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
#st.header("Quelques graphiques sur l'ensemble des données IMDB et TMDB")
col1, col2 = st.columns(2)
#col2.subheader("another one")
col1.plotly_chart(fig1, theme=None,use_container_width=True)
col1.plotly_chart(fig2, theme=None,use_container_width=True)
col2.plotly_chart(fig3, theme=None,use_container_width=True)
col2.plotly_chart(fig4, theme=None,use_container_width=True)



#my_bar = st.progress(0)
#for percent_complete in range(100):
#     time.sleep(0.01)
#     my_bar.progress(percent_complete + 1)
#my_bar.empty()
#st.balloons()



