from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
)
from blog.models import *
from blog.api.serializers import CommentSerializer, CreateCommentSerializer
from rest_framework.decorators import api_view

# Creates a new comment 
class CreateComment(CreateAPIView):
    serializer_class = CreateCommentSerializer

# list comments
class ListComment(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# Update a comment
class UpdateComment(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer

    # 'UpdateComment' should either include a `queryset` attribute, or override the `get_queryset()` method.
    def get_queryset(self):
        return Comment.objects.all()

# delete a comment
class DeleteComment(RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
            return Comment.objects.all()

# like a comment
