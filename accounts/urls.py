from django.urls import path
from . import views


urlpatterns = [
    path('profile/<username>/', views.profile),
    path('update/<username>/', views.update_firstname),
    path('<user_name>/follow/', views.follow),
    path('<user_name>/follow_info/', views.follow_info),
]