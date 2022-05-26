from django.urls import path
from . import views


urlpatterns = [
    path('', views.review_index), 
    path('<int:movie_id>/review_create/', views.review_create), 
    path('<int:movie_id>/review_all/', views.review_all),
    path('<int:review_pk>/', views.review_detail),
    path('<int:review_pk>/review_like/', views.review_like),
    path('<int:review_pk>/like_users/', views.review_like_users), 
    path('<int:review_pk>/review_comments/', views.review_comment_cr),
    path('<int:review_pk>/review_comments/<int:review_comment_pk>/', views.review_comment_ud),
]