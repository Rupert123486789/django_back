from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Review, Review_Comment

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):

    class ReviewCommentSerializer(serializers.ModelSerializer):

        class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ('id', 'username')

        user = UserSerializer(read_only=True)

        class Meta:
            model = Review_Comment
            fields = '__all__'
    
    review_comments = ReviewCommentSerializer(many=True, read_only=True)
    review_comments_count = serializers.IntegerField(source='review_comments.count', read_only=True)

    class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ('id', 'username')

    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'like_users', 'user',)


class ReviewListSerailizer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username')

    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class ReviewLikeUserSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')

    like_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Review
        fields = ('id', 'like_users',)