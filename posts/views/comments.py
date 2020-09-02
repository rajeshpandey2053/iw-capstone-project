from .posts import *
from ..models import Comment
from ..serializers import CommentSerializer, CreateCommentSerializer
from ..paginations import CustomCommentsPagination
from ..models import Post
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ListComments(ListAPIView):
    """
    This view returns gives the five comments at a time of respective posts
    """
    http_method_names = [u'get', ]
    lookup_field = 'post_slug'
    lookup_url_kwarg = 'post_slug'
    serializer_class = CommentSerializer
    pagination_class = CustomCommentsPagination

    def get_queryset(self):
        post = Post.objects.get(post_slug=self.kwargs[self.lookup_url_kwarg])
        print(post)
        return Comment.objects.filter(post=post)


class CreateComment(CreateAPIView):
    """
    This creates a new comment and saves to the database.
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = CreateCommentSerializer


class UpdateComment(RetrieveUpdateAPIView):
    """
    This should update the comment.
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = CreateCommentSerializer

    def get_queryset(self):
        return Comment.objects.all()


class RetrieveDeleteComment(RetrieveDestroyAPIView):
    """
    This retrieves the comment with get request and deletes with delete request.
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def like_comment(request, pk, action):
    comment = Comment.objects.get(pk=pk)
    try:
        print(comment)
    except comment.model.DoesNotExist:
        return Response({'error': 'The comment does not exist.'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if action == 'like':
            comment.stars_count += 1
            comment.save()
        elif action == 'unlike':
            comment.stars_count -= 1
            if comment.stars_count <= 0:
                comment.stars_count = 0
            comment.save()
        else:
            return Response({'error': f'Invalid action {action}!!'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'GET method not allowed!'},
                    status=status.HTTP_400_BAD_REQUEST)
