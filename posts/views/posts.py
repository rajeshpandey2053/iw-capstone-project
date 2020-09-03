import uuid

from django.utils.text import slugify
from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     RetrieveUpdateAPIView,
                                     UpdateAPIView,
                                     RetrieveDestroyAPIView)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes
                                       )
from ..models import Post
from ..serializers import (PostSerializer, CreatePostSerializer)
from ..paginations import CustomPostsPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models.profile import Profile
from django.contrib.auth import get_user_model

USER = get_user_model()


class ListPosts(ListAPIView):
    """
    This view is paginated to return a list of 15 posts at a time.
    """
    http_method_names = [u'get', ]
    serializer_class = PostSerializer
    pagination_class = CustomPostsPagination
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Post.objects.all()


class CreatePost(CreateAPIView):
    """
    Creates a New Post
    """
    serializer_class = CreatePostSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        """
        The original function overridden so that the post slug is generated
        automatically and is unique.
        """
        data = request.data.copy()
        # copying the dict because the original QueryDict is immutable.
        print("purano data", data)
        data[
            'post_slug'] = f'{slugify(data["caption"][:10])}-{uuid.uuid4().hex}'
        user = USER.objects.get(email=request.user)
        data["user"] = user.id
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class UpdatePost(UpdateAPIView):
    """
    Retrieves and updates a new post with post_slug as url kwarg.
    """
    lookup_field = 'post_slug'
    lookup_url_kwarg = 'post_slug'
    serializer_class = CreatePostSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Post.objects.all()

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        # copying the dict because the original QueryDict is immutable.
        print("purano data", data)
        data[
            'post_slug'] = f'{slugify(data["caption"][:10])}-{uuid.uuid4().hex}'
        user = USER.objects.get(email=request.user)
        print(user.id)
        data["user"] = user.id
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RetrieveDeletePost(RetrieveDestroyAPIView):
    """
    Deletes the post with matching post_slug in url kwarg.
    """
    lookup_field = 'post_slug'
    lookup_url_kwarg = 'post_slug'
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Post.objects.all()


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def like_post(request, post_slug, action):
    print(request.user)
    post = Post.objects.get(post_slug=post_slug)
    profile = Profile.objects.get(user=request.user)
    try:
        print(post)
    except post.model.DoesNotExist:
        return Response({'error': 'The post does not exist.'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if action == 'like':
            profile.post.add(post)
            post.stars_count += 1
            print(post.stars_count)
            post.save()
        elif action == 'unlike':
            profile.post.remove(post)
            post.stars_count -= 1
            if post.stars_count <= 0:
                post.stars_count = 0
            post.save()
            print(post.stars_count)
        else:
            return Response({'error': f'Invalid  {action}!!'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PostSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'GET method not allowed!'},
                    status=status.HTTP_400_BAD_REQUEST)


class FollowedPosts(ListPosts):
    """
    This is the view that returns the list of posts that are followed by the
    person.
    """
    serializer_class = PostSerializer
    pagination_class = CustomPostsPagination

    def get_queryset(self):
        return Post.objects.all()
