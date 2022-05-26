import os
from dotenv import load_dotenv   
import requests
import json

load_dotenv()
TMDB_API_KEY  = str(os.getenv('TMDB_API_KEY'))

GENRE_URL = f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=ko-kr'

genres_response = requests.get(GENRE_URL)
genres = genres_response.json()
print(genres)

total_genres_data = []

for genre in genres['genres']:
    genres_fields = {        
        'name': genre['name'],
    }
    genres_data = {
        'pk': genre['id'],
        'model': 'movies.genres',
        'fields': genres_fields
    }
    total_genres_data.append(genres_data)
print(total_genres_data)

with open('genres.json', 'w', encoding='utf-8') as w:
        json.dump(total_genres_data, w, indent="\t", ensure_ascii=False)