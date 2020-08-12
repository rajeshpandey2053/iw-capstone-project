from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import (CreateAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (UserRegisterSerializer,
                          UserUpdateSerializer)


User = get_user_model()


class UserDetail(RetrieveAPIView):
    """
    API end point to retrieve the user object
    who is currently active
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        """
        returns the user detail
        :return: JSON response of user detail
        """
        user = User.objects.get(id=request.user.id)
        user_data = UserRegisterSerializer(user)
        return Response(user_data.data, status=status.HTTP_302_FOUND)


class UserUpdate(UpdateAPIView):
    """
    API end point to update the user object
    who is currently active
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        """partially updating the user"""

        partial = kwargs.pop('partial', False)
        instance = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.profile_pic = request.FILES.get('profile_pic')
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(CreateAPIView):
    """API view for User Registration"""
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """accepting post request and serializer validation"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'message': "User successfully created"
        }
        return Response(response, status=status.HTTP_201_CREATED)