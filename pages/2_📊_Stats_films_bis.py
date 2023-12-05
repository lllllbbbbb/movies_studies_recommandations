# IMPORTS
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
st.set_page_config(
    page_title="Dashboard Projet 2",
    page_icon="📈",
    layout="wide",
)
#st.title('KPIs Cinema (bis)')
st.markdown("<h1 style='text-align: center; color: white;'>Quelques graphiques sur l'ensemble des données IMDB et TMDB (bis)</h1>", unsafe_allow_html=True)
#importation de la table movies
movies = pd.read_parquet('movies.parquet.gzip')

#Groupement par 'startYear' et 'genre1' et comptage du nombre de tconst pour chaque groupe
movies_startyear = movies.groupby(['startYear', 'genre1']).size().reset_index(name='Nombre_de_films')
movies_startyear['startYear'] = movies_startyear['startYear'].astype(int)

#Calculer les occurrences des genres et trier par ordre décroissant
genre_counts = movies_startyear['genre1'].value_counts().sort_values(ascending=False)

fig = px.scatter(movies_startyear, x='startYear', y='Nombre_de_films', color = 'genre1', title='Distribution des genres par année',
                 labels={'startYear': 'Année', 'genre1': 'Genre', 'Nombre_de_films':'Nombre de films'},
                width=1000, height=600,
                 category_orders={'genre1': genre_counts.index.tolist()}
                )
fig.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
st.plotly_chart(fig, theme=None, use_container_width=True)