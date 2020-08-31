from rest_framework import serializers
from .models import Comment, Post
from django.contrib.auth import get_user_model
from accounts.api.serializers import EducationSerializer
from accounts.models.education import Education

USER = get_user_model()


class PostEducationSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ['university', "semester", "faculty"]


class PostSerializer(serializers.ModelSerializer):
    education = PostEducationSerialzer()
    user = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = Post
        fields = ["posted_at", "modified_at", "user", "post_slug",
                  "caption", "file", "stars_count", "user_name", "id", 'education']
        read_only_fields = ['user_name', "id"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ['post', 'user', 'comment_description', 'commented_at',
                  'comment_modified_at', 'stars_count', 'user_name', 'id']
        read_only_fields = ['user_name', 'id']


class CreatePostSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    education = PostEducationSerialzer()

    class Meta:
        model = Post
        fields = ['user', 'post_slug', 'caption', 'file',
                  'education', 'posted_at', 'modified_at', "user_name"]

        read_only_fields = ['user_name', 'posted_at', 'modified_at']

    @staticmethod
    def get_user_name(obj):
        user = USER.objects.get(email=obj.user)
        return user.username

    def create(self, validated_data):
        print(validated_data)
        education_data = validated_data.pop('education')
        education, created = Education.objects.get_or_create(**education_data)
        post = Post.objects.create(
            user=validated_data['user'],
            post_slug=validated_data['post_slug'],
            caption=validated_data['caption'],
            file=validated_data['file'],
            education=education
        )
        return post

    def update(self, instance, validated_data):
        print(validated_data)
        education_data = validated_data.pop('education')
        instance.user = validated_data['user']
        instance.post_slug = validated_data['post_slug']
        instance.caption = validated_data['caption']
        instance.file = validated_data['file']
        instance.education.semester = education_data['semester']
        instance.education.faculty = education_data['faculty']
        instance.education.university = education_data['university']
        instance.save()
        return instance


class CreateCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['post', 'user', 'comment_description', 'commented_at',
                  'comment_modified_at', 'stars_count', 'user_name', 'id']
        read_only_fields = ['stars_count', 'id', 'user_name']

    @staticmethod
    def get_user_name(obj):
        user = USER.objects.get(email=obj.user)
        return user.username
