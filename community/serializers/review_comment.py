from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Review_Comment

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username')

    user = UserSerializer(read_only=True)

    class Meta:
        model = Review_Comment
        fields = '__all__'
        read_only_fields = ('review', 'user')


