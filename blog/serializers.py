from rest_framework import serializers
from .models import Post, Comment


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = 'id author title created_at updated_at is_published'.split()


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = 'id author title body created_at updated_at is_published'.split()
        read_only_fields = 'id author created_at updated_at'.split()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = 'id post author body created_at updated_at is_approved'.split()
        read_only_fields = 'id post author created_at updated_at is_approved'.split()
