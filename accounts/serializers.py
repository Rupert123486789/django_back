from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from movies.serializers.movie import MovieSerializer



class ProfileSerializer(serializers.ModelSerializer):

    
    # like_movies_genres = serializers.CharField(source='like_movies.all', read_only=True)
    like_movies = MovieSerializer(many=True, read_only=True)   
    pick_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        exclude = ('email',) 

class ProfileUpdateSerializer(serializers.ModelSerializer):    

    class Meta:
        model = get_user_model()
        fields = ('first_name',)
        #exclude = ('email',) 


class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    first_name = serializers.CharField(
        max_length=150,
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')

        return data
        

class FollowSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = ('id', 'username')


    followers = UserSerializer(read_only=True, many=True)
    followings = UserSerializer(read_only=True, many=True)
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'