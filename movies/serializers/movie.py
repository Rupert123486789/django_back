from rest_framework import serializers
from django.contrib.auth import get_user_model

from ..models import Info, Movie, Genre, Actor, Director, Movie_Comment

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = '__all__'

    class DirectorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Director
            fields = '__all__'

    class MovieCommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie_Comment
            fields = '__all__'

    
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)
    directors = DirectorSerializer(many=True)
    movie_comments = MovieCommentSerializer(many=True)
    movie_comments_count = serializers.IntegerField(source='movie_comments.count', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'


class MovieLikeUserSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')

    like_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('id', 'like_users',)

class MoviePickUserSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')

    pick_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('id', 'pick_users',)


class InfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Info
        fields = "__all__"
        