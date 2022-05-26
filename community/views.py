from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view

from .serializers.review import ReviewListSerailizer, ReviewSerializer, ReviewLikeUserSerializer
from .serializers.review_comment import CommentSerializer

from .models import Review, Review_Comment
from movies.models import Movie


@api_view(['GET'])
def review_index(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewListSerailizer(reviews, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def review_create(request, movie_id):
    if request.method == 'POST':
        user = request.user
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def review_all(request, movie_id):
    reviews = Review.objects.filter(movie_id=movie_id)
    serializer = ReviewListSerailizer(reviews, many=True)
    return Response(serializer.data)



@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        data = {
            'delete': f'{review_pk}번 review가 삭제 되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user
    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    else:
        review.like_users.add(user)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


@api_view(['GET'])
def review_like_users(request, review_pk):
	review = get_object_or_404(Review, pk=review_pk)
	serializer = ReviewLikeUserSerializer(review)
	return Response(serializer.data) 
        

@api_view(['GET','POST'])
def review_comment_cr(request, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        comments = review.review_comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, user=user)
            # comments = review.review_comments.all()
            # serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def review_comment_ud(request, review_pk, review_comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    review_comment = get_object_or_404(Review_Comment, pk=review_comment_pk)
    if request.method == 'PUT':
        if request.user == review_comment.user:
            serializer = CommentSerializer(instance=review_comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                # comments = review.review_comments.all()
                # serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user == review_comment.user:
            review_comment.delete()
            # comments = review.review_comments.all()
            # serializer = CommentSerializer(comments, many=True)
            data = {
                'delete': f'{review_comment_pk}번 댓글이 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)