from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer
)


class CustomPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


def get_posts_for_user(user):
    posts = Post.objects.select_related('author').order_by('-created_at')
    if user.is_authenticated:
        return posts.filter(Q(is_published=True) | Q(author=user))
    return posts.filter(is_published=True)


def get_post_or_404(id, user):
    try:
        post = Post.objects.select_related('author').get(id=id)
    except Post.DoesNotExist:
        return None
    if post.is_published or post.author == user:
        return post
    return None


@swagger_auto_schema(method='post', request_body=PostDetailSerializer)
@api_view(['GET', 'POST'])
def post_list_api_view(request):
    if request.method == 'GET':
        posts = get_posts_for_user(request.user)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = PostListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = PostDetailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    post = serializer.save(author=request.user)
    return Response(
        data=PostDetailSerializer(post).data,
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(method='put', request_body=PostDetailSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail_api_view(request, id):
    post = get_post_or_404(id, request.user)
    if post is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(data=PostDetailSerializer(post).data)

    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if post.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = PostDetailSerializer(post, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)


@swagger_auto_schema(method='post', request_body=CommentSerializer)
@api_view(['GET', 'POST'])
def comment_list_api_view(request, id):
    post = get_post_or_404(id, request.user)
    if post is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments = post.comments.select_related('author').order_by('-created_at')
        if request.user.is_authenticated:
            comments = comments.filter(Q(is_approved=True) | Q(author=request.user))
        else:
            comments = comments.filter(is_approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data)

    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    comment = serializer.save(post=post, author=request.user)
    return Response(
        data=CommentSerializer(comment).data,
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(method='put', request_body=CommentSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail_api_view(request, id):
    try:
        comment = Comment.objects.select_related('author', 'post').get(id=id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not comment.post.is_published and comment.post.author != request.user:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if comment.is_approved or comment.author == request.user:
            return Response(data=CommentSerializer(comment).data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if comment.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CommentSerializer(comment, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)
