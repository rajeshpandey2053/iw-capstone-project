from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    # explore
    path('v1/post/explore/', views.ListPosts.as_view(), name='posts_explore'),

    # posts
    path('v1/post/list/', views.FollowedPosts.as_view(), name='posts_list'),
    path('v1/post/create/', views.CreatePost.as_view(), name='post_create'),
    # The below url can view and delete the post with get and delete method.
    path('v1/post/<str:post_slug>/', views.RetrieveDeletePost.as_view(),
         name='post_get_delete'),
    path('v1/post/<str:post_slug>/update/', views.UpdatePost.as_view(),
         name='post_update'),
    # like post api
    path('v1/post/<str:post_slug>/<str:action>/', views.like_post,
         name='like_unlike_post'),
    # comments
    path('v1/comment/<str:post_slug>/list/',
         views.ListComments.as_view(), name='comment_list'),
    path('v1/comment/create/', views.CreateComment.as_view(),
         name='comment_create'),
    path('v1/comment/<str:pk>/update/', views.UpdateComment.as_view(),
         name='comment_update'),
    path('v1/comment/<str:pk>/', views.RetrieveDeleteComment.as_view(),
         name='comment_get_delete'),
    path('v1/comment/<str:pk>/<str:action>/', views.like_comment,
         name='like_unlike_comment'),
]
