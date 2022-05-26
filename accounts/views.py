from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from accounts import serializers



User = get_user_model()

@api_view(['GET'])
def profile(request, username):
    user = get_object_or_404(User, username=username)
    serializer = ProfileSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
def update_firstname(request, username):
    print(request.method)
    user = get_object_or_404(User, username=username)
    serializer = ProfileUpdateSerializer(instance=user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
def follow(request, user_name):
    you = get_object_or_404(get_user_model(), username=user_name)
    me = request.user
    if you != me:
        if you.followers.filter(pk=request.user.pk).exists():
            you.followers.remove(me)
            return Response({'data': f'{user_name}님을 팔로우 취소하였습니다.', 'follow': False})
        else:
            you.followers.add(me)
            return Response({'data': f'{user_name}님을 팔로우하였습니다.', 'follow': True})


@api_view(['GET'])
def follow_info(request, user_name):
    me = get_object_or_404(get_user_model(), username = user_name)    
    serializer = FollowSerializer(me)    
    return Response(serializer.data)  