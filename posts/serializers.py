from rest_framework import serializers
from .models import Comment, Post
from django.contrib.auth import get_user_model

USER = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = Post
        fields = ["posted_at", "modified_at", "user", "post_slug",
                  "caption", "file", "stars_count", "user_name", "id"]
        read_only_fields = ['user_name', "id"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ['post', 'user', 'comment_description', 'commented_at',
                  'comment_modified_at', 'comment_description', 'stars_count', 'user_name', 'id']
        read_only_fields = ['user_name', 'id']


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'post_slug', 'caption', 'file']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user', 'comment_description', ]
