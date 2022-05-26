import os
from dotenv import load_dotenv   
import requests
import json

load_dotenv()
TMDB_API_KEY  = str(os.getenv('TMDB_API_KEY'))

def get_movie_datas():
    total_movie_data = []
    total_actor_data = []
    total_director_data = []
    total_genre_data = []

    for i in range(1, 25):      
        
        MOVIE_URL = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-kr&page={i}'
        movies_response = requests.get(MOVIE_URL)
        # print(response.status_code, response.url)
        movies = movies_response.json()
        # print(movies['results'])
        # print(len(movies.get('results')))    
        
        for movie in movies['results']:

            movie_fields = {                
                'title': movie['title'],
                'overview': movie['overview'],
                'release_date': movie['release_date'],
                'popularity': movie['popularity'],
                'vote_average': movie['vote_average'] * 0.5,
                'poster_path': movie['poster_path'],
                'adult': movie['adult'],
                'youtube_key': '',
                'actors': [],
                'directors': [],
                'genres': [],
                }

            movie_id = movie['id']       
            print(movie['title'])
            VIDEOS_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=ko-kr'
            videos_response = requests.get(VIDEOS_URL)
            videos = videos_response.json()
            
            for video in videos['results']:
                movie_fields['youtube_key'] = video['key']
                break
            # print(movie_fields)

            CREDITS_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-kr'
            credits_response = requests.get(CREDITS_URL)
            credits = credits_response.json()
            
            # 배우 정보(상위 5명)            
            cnt = 0
            for cast in credits['cast']:
                actor_fields = {
                    'name': cast['name'],
                    'profile_path': cast['profile_path']
                }
                actor_data = {
                    'pk': cast['id'],
                    'model': 'movies.actor',
                    'fields': actor_fields
                }
                total_actor_data.append(actor_data)
                
                movie_fields['actors'].append(cast['id'])
                cnt += 1               
                if cnt == 5:
                    break
            # print(actor_fields)

            # 제작진 정보(감독만)
            for crew in credits['crew']:
                if crew['job'] == 'Director':
                    director_fields = {
                        'name': crew['name'],
                        'profile_path': crew['profile_path']
                    }
                    director_data = {
                        'pk': crew['id'],
                        'model': 'movies.director',
                        'fields': director_fields
                    }
                    total_director_data.append(director_data)
                
                    movie_fields['directors'].append(crew['id'])
                    
            
            DETAILS_URL = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko-kr'
            details_response = requests.get(DETAILS_URL)
            details = details_response.json()
            # 장르 정보          
            for genre in details['genres']:
                genre_fields = {
                    'name': genre['name'],
                }
                genre_data = {
                    'pk': genre['id'],
                    'model': 'movies.genre',
                    'fields': genre_fields
                }
                total_genre_data.append(genre_data)
                
                movie_fields['genres'].append(genre['id'])



            movie_data = {
                'pk': movie['id'],
                'model': 'movies.movie',
                'fields': movie_fields
            }
            
            total_movie_data.append(movie_data)
            

    with open('movie_data.json', 'w', encoding='utf-8') as w:
        json.dump(total_movie_data, w, indent="\t", ensure_ascii=False)
    with open('actor_data.json', 'w', encoding='utf-8') as w:
        json.dump(total_actor_data, w, indent="\t", ensure_ascii=False)
    with open('director_data.json', 'w', encoding='utf-8') as w:
        json.dump(total_director_data, w, indent="\t", ensure_ascii=False)
    with open('genre_data.json', 'w', encoding='utf-8') as w:
        json.dump(total_genre_data, w, indent="\t", ensure_ascii=False)


get_movie_datas()

