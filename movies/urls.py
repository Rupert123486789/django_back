from django.urls import path
from . import views


urlpatterns = [
    path('<int:movie_pk>/', views.movie_detail),
    path('genres/', views.genres_make),
    # path('interstellar/', views.interstellar_make),
    path('<int:movie_pk>/movie_like/', views.movie_like),
    path('<int:movie_pk>/like_users/', views.movie_like_users), 
    path('<int:movie_pk>/movie_pick/', views.movie_pick),
    path('<int:movie_pk>/pick_users/', views.movie_pick_users),  
    path('<int:movie_pk>/movie_comments/', views.movie_comment_cr),
    path('<int:movie_pk>/movie_comments/<int:movie_comment_pk>/', views.movie_comment_ud),
    path('all_movies/<type>/',views.get_all_movies),
    path('index/<username>/', views.movie_index),
    # path('recommend/sun/', views.sun_recommend), 
    path('recommend/like/<username>/', views.like_recommend),
    path('recommend/little_like/<username>/', views.little_like_recommend),
    path('recommend/color_test/<results>/', views.color_recommend),
]