from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView
)

from blog.models import *
from blog.api.serializers import BlogSerializer, CreateBlogSerializer

# list blog 
class ListBlog(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


# create a new blog
class CreateBlog(CreateAPIView):
    serializer_class = CreateBlogSerializer

# update a blog
class UpdateBlog(RetrieveUpdateAPIView):
    serializer_class = CreateBlogSerializer
    
    def get_queryset(self):
        return Blog.objects.all()

# delete a blog
class DeleteBlog(RetrieveDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
            return Blog.objects.all()

# like a blog