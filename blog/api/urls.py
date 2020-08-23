from django.urls import path
from ..views.comment import UpdateComment, DeleteComment, ListComment, CreateComment
from ..views.blog import CreateBlog, ListBlog, UpdateBlog, DeleteBlog


urlpatterns = [

    # blog
    path('v1/blog/create',CreateBlog.as_view(),name='create_blog'),
    path('v1/blog/list',ListBlog.as_view(),name='list_blog'),
    path('v1/blog/<int:pk>/update',UpdateBlog.as_view(),name='update_blog'),
    path('v1/blog/<int:pk>/delete',DeleteBlog.as_view(),name='delete_blog'),

    # Comment
    path('v1/comment/create',CreateComment.as_view(),name='create_comment'),
    path('v1/comment/list',ListComment.as_view(),name='list_comment'),
    path('v1/comment/<int:pk>/update',UpdateComment.as_view(),name='update_comment'),
    path('v1/comment/<int:pk>/delete',DeleteComment.as_view(),name='delete_comment'),
    
]
