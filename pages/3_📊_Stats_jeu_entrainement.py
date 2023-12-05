import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
st.set_page_config(
    page_title= "KPI's sur le Fichier Final",
    page_icon= "📈",
    layout="wide",)
#st.title('Indicateurs sur le Fichier Final - 10 736 Films')
st.markdown("<h1 style='text-align: center; color: white;'>Indicateurs sur le Fichier Final  - 4 758 films</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>---</h2>", unsafe_allow_html=True)

# CHARGEMENT DES DATAFRAMES

#df_final = pd.read_parquet('df_final.parquet.gzip')
df_french = pd.read_parquet('df_french_2.parquet.gzip')

# MODIFICATION DU DF_FINAL EN DF_GENRES, OU LE GENRE EST SPLITE ET "DECADE" CREE A PARTIR DE "STARTYEAR"
df_genres = df_french.copy()
df_genres['genre'] = df_genres['genres'].apply(lambda x: x.split(",")[0] if pd.notnull(x) else x)
df_genres['decade'] = df_genres['startYear'].apply(lambda x: (x//10)*10)

#CREATION DES DF GROUPBY POUR LES GRAPHES

df_decade = df_genres.groupby('decade').size().reset_index(name='Nombre_de_films')
df_genres_rating = df_genres.groupby(['averageRating', 'genre']).size().reset_index(name='Nombre_de_films')
df_genre_votes = df_genres.groupby('genre')['numVotes'].sum().reset_index(name='Total_numVotes')
df_genre_votes = df_genre_votes.sort_values(by='Total_numVotes', ascending=False)

df_decade_votes = df_genres.groupby('decade')['numVotes'].mean().reset_index(name='Total_numVotes')
df_decade_votes = df_decade_votes.sort_values(by='decade', ascending=False)

# CREATION DES GRAPHES
# Graphe 1 : Films par décennie
graph_nb_movies_by_decade = px.bar(df_decade, x='decade', y='Nombre_de_films', 
                                   labels={'decade': 'Décennies', 'Nombre_de_films': 'Nombre de films'},
                                   width=900, height=400,
                                   color_discrete_sequence =['#980321']
                                    )
graph_nb_movies_by_decade.update_layout(title={'text': 'Distribution du Nombre de Films par Décennie','x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
graph_nb_movies_by_decade.update_xaxes(title=None)

#palette_rouge = sns.color_palette("Reds", 17).as_hex()
palette_rouge = ['#FF0000', '#FF4500', '#B22222', '#8B0000', '#DC143C', '#FF6347', '#FFA07A', '#FA8072', '#E9967A', '#FF7F50', '#FF4500', '#CD5C5C', '#F08080', '#FF69B4', '#FF1493', '#C71585', '#DB7093']
# Graphe 2 : Films par Note Moyenne
graph_nb_movies_by_rating = px.bar(df_genres_rating, x='averageRating', y='Nombre_de_films', 
                                   color='genre',
                                   width=900, height=400,
                                   labels={'averageRating': 'Note Moyenne', 'Nombre_de_films': 'Nombre de films', 'genre': 'Genre'}, color_discrete_sequence=palette_rouge
                                  )
graph_nb_movies_by_rating.update_layout(title={'text': 'Distribution Nombre Films par Genre selon la Note Moyenne','x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
graph_nb_movies_by_rating.update_xaxes(title=None)
# Graphe 3 : Films par Log NumVotes
graph_nb_movies_by_LogVotes = px.bar(df_genre_votes, x='genre', y='Total_numVotes',
                                     labels={'genre': 'Genre', 'Total_numVotes': 'Nombre de votes (log)'},
                                     width=900, height=400,
                                     color_discrete_sequence =['#980321'],
                                     log_y = True
                                    )
graph_nb_movies_by_LogVotes.update_layout(title={'text': 'Distribution du Nombre de Votes par Genre','x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
graph_nb_movies_by_LogVotes.update_xaxes(tickangle=45)
graph_nb_movies_by_LogVotes.update_xaxes(title=None)
# Graphe 4 : Films par Moyenne de Votes selon les Décennies
graph_nb_movies_by_MeanVotes_Decade = px.line(df_decade_votes, x='decade', y='Total_numVotes',
                                              labels={'decade': 'Décennies', 'Total_numVotes': 'Nombre moyen de votes par décennie'},
                                              width=900, height=400,
                                              markers = True,
                                              color_discrete_sequence =['#D2002A']
                                             )
graph_nb_movies_by_MeanVotes_Decade.update_layout(title={'text': 'Nombre de Votes par Décennie','x': 0.5, 'xanchor': 'center', 'font': {'size': 24}})
graph_nb_movies_by_MeanVotes_Decade.update_xaxes(title=None)

fig3 = graph_nb_movies_by_decade
fig2 = graph_nb_movies_by_rating
fig1 = graph_nb_movies_by_LogVotes
fig4 = graph_nb_movies_by_MeanVotes_Decade
fig3.update_layout(showlegend=False)
fig2.update_layout(showlegend=True)
fig2.update_layout(template="seaborn")
fig4.update_traces(line=dict(width=3))
col1, col2 = st.columns(2)

col1.plotly_chart(fig1, theme=None,use_container_width=True)
col1.plotly_chart(fig2, theme=None,use_container_width=True)
col2.plotly_chart(fig3, theme=None,use_container_width=True)
col2.plotly_chart(fig4, theme=None,use_container_width=True)
