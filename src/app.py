import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# load the .env file variables
load_dotenv()


# Spotify API credentials
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

artist_id = "61C3cEhdoJ9YiQSQSwYB4K"
#artist_id = "5MmVJVhhYKQ86izuGHzJYA"  # Mika


#Top tracks de un artista por ID
results = spotify.artist_top_tracks(artist_id)

songs = []
for element in results['tracks']:
    minutos = element['duration_ms'] // 60000
    segundos = (element['duration_ms'] % 60000) // 1000
    if segundos < 10:
        segundos = f"0{segundos}"
    else:
        segundos = str(segundos)
    songs.append({
        'titulo': element['name'],
        'popularidad': element['popularity'],
        'duracion': f"{minutos}:{segundos}"
    })
#print(songs)


# Crear un DataFrame de las canciones y ordenar por popularidad
songs_df = pd.DataFrame(songs)
songs_df = songs_df.sort_values(by='popularidad', ascending=False)
print(songs_df.head(3))

# Relación la duración con la popularidad

def duracion_a_segundos(duracion):
    minutos, segundos = map(int, duracion.split(':'))
    return minutos * 60 + segundos

songs_df['duracion_segundos'] = songs_df['duracion'].apply(duracion_a_segundos) #Aplicar a la columna duracion el metodo de segundos

songs_df = songs_df.sort_values(by='duracion_segundos')

plt.scatter(songs_df['duracion'], songs_df['popularidad'])
plt.xlabel('Duration (minutes)')
plt.ylabel('Popularity')
plt.title('Relationship between duration and popularity')
plt.show()
