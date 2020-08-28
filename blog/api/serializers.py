from django.contrib.auth import get_user_model
from rest_framework import serializers
from blog.models import Category, Tag, Blog, Comment, Subscriber

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Comment
        fields = '__all__'

class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'name',
            'blog',
            'email',
            'message',
        ]