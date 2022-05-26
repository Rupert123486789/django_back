from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view

from .serializers.movie import InfoSerializer, MovieLikeUserSerializer, MovieListSerializer, MovieSerializer, MoviePickUserSerializer, GenreSerializer
from .serializers.movie_comment import CommentSerializer

from .models import Genre, Movie, Movie_Comment


from django.db.models import Count

from datetime import datetime
import random
# from .crawling import now_altitude, lat, lng, address


User = get_user_model()

@api_view(['GET'])
def movie_index(request, username):
	user = get_object_or_404(User, username=username)
	
	movies = get_list_or_404(Movie)	
	current_time = datetime.now()
	
	if user.time == None or user.visit_count == None:
		user.time = current_time
		user.visit_count = 1
		user.save()	
	
	if (user.time.day != current_time.day) or (user.time.month != current_time.month) or (user.time.year != current_time.year):
		user.visit_count += 1
		user.time = current_time
		user.save()

	serializer = MovieListSerializer(movies, many=True)			
	return Response(serializer.data)



@api_view(['GET'])
def get_all_movies(request, type):
    
    if type == 'all':
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    
    elif type == 'vote_average':
        #평점순
        movies = Movie.objects.order_by('-vote_average')[0:10]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    elif type == 'popularity':
        #인기순(종합적지표)
        movies = Movie.objects.order_by('-popularity')[0:10]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
        
    elif type == 'release_date':
        # 최신순
        movies = Movie.objects.order_by('-release_date')[0:10]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    elif type == 'adult':
        #성인영화
        movies = Movie.objects.filter(adult='True').order_by('?')[0:10]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    elif type == 'like_cnt':
        #좋아요순
        like_cnt = Movie.objects.annotate(Count('like_users'))
        movies = like_cnt.order_by('-like_users__count')
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    elif type == 'pick_cnt':
        #픽순
        pick_cnt = Movie.objects.annotate(Count('pick_users'))
        movies = pick_cnt.order_by('-pick_users__count')
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
        
    


@api_view(['GET'])
def movie_detail(request, movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_pk)
        movie_a = [movie]
        serializer = MovieSerializer(data=movie_a, many=True)
        genres = movie.genres.all().values_list('id', flat=True)
        movies_same_genre = Movie.objects.filter(genres__id__in=genres).prefetch_related('genres').distinct().order_by('-vote_average')[:5]
        same_genre_serializer = MovieSerializer(data=movies_same_genre, many=True)
        print(serializer.is_valid(), same_genre_serializer.is_valid())
        data = {
            'movie': serializer.data,
            'same_genre': same_genre_serializer.data
        }
        return Response(data)

@api_view(['GET'])
def genres_make(request):    
    genres_json = [
	{
		"pk": 28,
		"model": "movies.genres",
		"fields": {
			"name": "액션"
		}
	},
	{
		"pk": 12,
		"model": "movies.genres",
		"fields": {
			"name": "모험"
		}
	},
	{
		"pk": 16,
		"model": "movies.genres",
		"fields": {
			"name": "애니메이션"
		}
	},
	{
		"pk": 35,
		"model": "movies.genres",
		"fields": {
			"name": "코미디"
		}
	},
	{
		"pk": 80,
		"model": "movies.genres",
		"fields": {
			"name": "범죄"
		}
	},
	{
		"pk": 99,
		"model": "movies.genres",
		"fields": {
			"name": "다큐멘터리"
		}
	},
	{
		"pk": 18,
		"model": "movies.genres",
		"fields": {
			"name": "드라마"
		}
	},
	{
		"pk": 10751,
		"model": "movies.genres",
		"fields": {
			"name": "가족"
		}
	},
	{
		"pk": 14,
		"model": "movies.genres",
		"fields": {
			"name": "판타지"
		}
	},
	{
		"pk": 36,
		"model": "movies.genres",
		"fields": {
			"name": "역사"
		}
	},
	{
		"pk": 27,
		"model": "movies.genres",
		"fields": {
			"name": "공포"
		}
	},
	{
		"pk": 10402,
		"model": "movies.genres",
		"fields": {
			"name": "음악"
		}
	},
	{
		"pk": 9648,
		"model": "movies.genres",
		"fields": {
			"name": "미스터리"
		}
	},
	{
		"pk": 10749,
		"model": "movies.genres",
		"fields": {
			"name": "로맨스"
		}
	},
	{
		"pk": 878,
		"model": "movies.genres",
		"fields": {
			"name": "SF"
		}
	},
	{
		"pk": 10770,
		"model": "movies.genres",
		"fields": {
			"name": "TV 영화"
		}
	},
	{
		"pk": 53,
		"model": "movies.genres",
		"fields": {
			"name": "스릴러"
		}
	},
	{
		"pk": 10752,
		"model": "movies.genres",
		"fields": {
			"name": "전쟁"
		}
	},
	{
		"pk": 37,
		"model": "movies.genres",
		"fields": {
			"name": "서부"
		}
	}
]
    return JsonResponse(genres_json, safe=False)


@api_view(['POST'])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        movie.like_users.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


@api_view(['GET'])
def movie_like_users(request, movie_pk):
	movie = get_object_or_404(Movie, pk=movie_pk)
	serializer = MovieLikeUserSerializer(movie)
	return Response(serializer.data) 


@api_view(['POST'])
def movie_pick(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if movie.pick_users.filter(pk=user.pk).exists():
        movie.pick_users.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        movie.pick_users.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

@api_view(['GET'])
def movie_pick_users(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MoviePickUserSerializer(movie)
    return Response(serializer.data) 
        

@api_view(['GET', 'POST'])
def movie_comment_cr(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        comments = movie.movie_comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            # comments = movie.movie_comments.all()
            # serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def movie_comment_ud(request, movie_pk, movie_comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_comment = get_object_or_404(Movie_Comment, pk=movie_comment_pk)
    if request.method == 'PUT':
        if request.user == movie_comment.user:
            serializer = CommentSerializer(instance=movie_comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                # comments = movie.movie_comments.all()
                # serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user == movie_comment.user:
            movie_comment.delete()
            # comments = movie.movie_comments.all()
            # serializer = CommentSerializer(comments, many=True)
            data = {
                'delete': f'{movie_comment_pk}번 댓글이 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def sun_recommend(request):
#     sun_altitude = now_altitude  
    

#     recommend_genres = []
#     if -90 <= int(sun_altitude) < -60:
#         recommend_genres = [27, 878, 53]
#     elif -60 <= int(sun_altitude) < -30:
#         recommend_genres = [10402, 9648, 10770]
#     elif -30 <= int(sun_altitude) < -0:
#         recommend_genres = [18, 36, 10749]
#     elif 0 <= int(sun_altitude) < 30:
#         recommend_genres = [12, 16, 14, 37]
#     elif 30 <= int(sun_altitude) < 60:
#         recommend_genres = [28, 35, 10751]
#     elif 60 <= int(sun_altitude) <= 90:
#         recommend_genres = [80, 99, 10752]

#     recommend_movies = set()
#     for recommend_genre in recommend_genres:
#         try:
#             genre = get_object_or_404(Genre, pk=recommend_genre)			
#             movies = genre.genre_movies.all()
#             recommend_movies.update(movies)
#         except:
#             continue
   

#     # 현재 데이터가 적어서 추천해줄 장르가 5개가 안되면 오류남
#     # 데이터 500개 받으면 해결될듯(추후 확인 필요)
#     recommend_movies_random = random.sample(list(recommend_movies), 5)
#     serializer1 = MovieSerializer(recommend_movies_random, many=True)
#     info = {
#         'latitude' : lat,
#         'longitude' : lng,
#         'address' : address
#     }
#     serializer2 = InfoSerializer(info)
#     return Response([serializer1.data, serializer2.data])


@api_view(['GET'])
def like_recommend(request, username):
	user = get_object_or_404(User, username=username)
	like_movies = user.like_movies.all()
	like_genres = {}
	for like_movie in like_movies:
		like_genre =  like_movie.genres.all()
		for genre in like_genre:
			if genre in like_genres:
				like_genres[genre] += 1
			else:
				like_genres[genre] = 1
	
	like_genres = sorted(like_genres.items(), key=lambda x: -x[1])
	
	recommend_genres = []
	cnt = 0 
	for genre in like_genres:
		recommend_genres.append(genre[0])
		cnt += 1
		if cnt == 2:
			break

	recommend_movies = Movie.objects.all()
	for genre in recommend_genres:
		# print(genre)
		# print(recommend_movies)
		recommend_movies = recommend_movies.filter(genres=genre)
	recommend_movies = recommend_movies[:5]
	# print(recommend_movies)
	serializer = MovieSerializer(recommend_movies, many=True)
	return Response(serializer.data)
	

@api_view(['GET'])
def little_like_recommend(request, username):
	user = get_object_or_404(User, username=username)
	like_movies = user.like_movies.all()
	like_genres = {}
	for like_movie in like_movies:
		like_genre =  like_movie.genres.all()
		for genre in like_genre:
			if genre in like_genres:
				like_genres[genre] += 1
			else:
				like_genres[genre] = 1
	
	like_genres = sorted(like_genres.items(), key=lambda x: x[1])
	
	recommend_genres = []
	
	for genre in like_genres:
		recommend_genres.append(genre[0])	
		break

	recommend_movies = Movie.objects.all()
	for genre in recommend_genres:
		# print(genre)
		# print(recommend_movies)
		recommend_movies = recommend_movies.filter(genres=genre)
	recommend_movies = recommend_movies[:5]
	# print(recommend_movies)
	serializer = MovieSerializer(recommend_movies, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def color_recommend(request, results):
	color = int(results)

	recommend_genres = []
	if -4 <= color < -2:
		recommend_genres = [27, 9648, 53, 10752]
	elif -2 <= color < 0:
		recommend_genres = [80, 99, 18, 10751, 36]
	elif 0 <= color < 2:
		recommend_genres = [16, 35, 14, 10402, 10770, 37]
	elif 2 <= color <= 4:
		recommend_genres = [28, 12, 10749, 878]

	recommend_movies = set()
	for recommend_genre in recommend_genres:
		try:
			genre = get_object_or_404(Genre, pk=recommend_genre)			
			movies = genre.genre_movies.all()
			recommend_movies.update(movies)
		except:
			continue
	
	# 현재 데이터가 적어서 추천해줄 장르가 5개가 안되면 오류남
	# 데이터 500개 받으면 해결될듯(추후 확인 필요)
	recommend_movies_random = random.sample(list(recommend_movies), 5)
	serializer = MovieSerializer(recommend_movies_random, many=True)
	return Response(serializer.data)