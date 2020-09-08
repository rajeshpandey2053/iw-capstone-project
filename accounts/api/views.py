from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView, DestroyAPIView, ListCreateAPIView)
from accounts.models import University, Faculty
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .utils import Util
from .serializers import (UserRegisterSerializer,
                          UserUpdateSerializer,
                          ChangePasswordSerializer,
                          ResetPasswordEmailRequestSerializer,
                          SetNewPasswordSerializer, UserFollowSerializer,
                          FacultySerializer, UniversitySerializer
                          )
from .tokens import account_activation_token
from accounts.models import UserFollow
from accounts.models.profile import Profile
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
        followers = UserFollow.objects.filter(follow_to=user).count()
        following = UserFollow.objects.filter(follow_by=user).count()
        user_data = UserRegisterSerializer(user)
        profile = Profile.objects.get(user=request.user)
        print(profile)
        context = {
            'user': user_data.data,
            'followers': followers,
            'following': following,
        }
        return Response(context, status=status.HTTP_200_OK)


class GetUserDetail(RetrieveAPIView):
    """
    API end point to retrieve the user object
    who is currently active
    """
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        """
        returns the user detail
        :return: JSON response of user detail
        """
        user = User.objects.get(id=kwargs[self.lookup_url_kwarg])
        followers = UserFollow.objects.filter(follow_to=user).count()
        following = UserFollow.objects.filter(follow_by=user).count()
        user_data = UserRegisterSerializer(user)
        profile = Profile.objects.get(user=request.user)
        print(profile)
        context = {
            'user': user_data.data,
            'followers': followers,
            'following': following,
        }
        return Response(context, status=status.HTTP_200_OK)


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
        print(request.data)
        partial = kwargs.pop('partial', False)
        instance = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
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
        user = serializer.save()
        # current_site = get_current_site(self.request)
        mail_subject = "Activate your Hamro Note Account"
        message = render_to_string('account_activate_email.html', {
            'user': user,
            'domain': 'iw-acad-hamro-note-fe.vercel.app',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        to_email = serializer.validated_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        response = {
            'success': True,
            'message': "Please Activate your account before proceeding"
        }
        return Response(response, status=status.HTTP_201_CREATED)


@api_view(('GET',))
def activate(request, uidb64, token):
    """User activation function"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        response = {
            'status': 'Success',
            'message': "User successfully activated. Please login now"
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            'status': 'Failed',
            'message': "Either the token is expired or you are not registered yet"
        }
        return Response(response, status=403)


class UserLogoutView(DestroyAPIView):
    """removing the token from the database"""
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = Token.objects.get(user=request.user)
        self.perform_destroy(instance)
        context = {
            'message': "Successfully Logged Out"
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(GenericAPIView):
    """
    API endpoint for requesting reset password.
    """
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(request=request).domain
            # relativeLink = reverse(
            #     'accounts:password-reset-confirm',
            #     kwargs={'uidb64': uidb64, 'token': token}
            # )
            absurl = f'https://iw-acad-hamro-note-fe.vercel.app/new-password/{uidb64}/{token}'
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your passsword'
            }
            Util.send_email(data)
        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )


class PasswordTokenCheckAPI(GenericAPIView):
    """
    API endpoint for checking token obtained after email has been sent to user
    """
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token is not valid, please request a new one'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            return Response(
                {
                    'success': True,
                    'message': 'Credentials Valid',
                    'uidb64': uidb64,
                    'token': token
                },
                status=status.HTTP_200_OK
            )

        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token is not valid, please request a new one'},
                    status=status.HTTP_401_UNAUTHORIZED
                )


class SetNewPasswordAPIView(GenericAPIView):
    """
    API endpoint for resetting new password.
    """
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'success': True, 'message': 'Password reset success'},
            status=status.HTTP_200_OK
        )


class UserFollowAPIView(ListCreateAPIView):
    """
    API end point for letting user to follow each other
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserFollowSerializer

    def get_queryset(self, *args, **kwargs):
        follow = UserFollow.objects.filter(follow_to=self.request.user)
        return follow

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # copying the dict because the original QueryDict is immutable.
        print("purano data", data)
        data['follow_by'] = request.user.id
        print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = {
            'message': 'success',
        }
        return Response(context, status.HTTP_201_CREATED)


class FacultyAPIView(ListAPIView):
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAuthenticated, ]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class UniversityAPIView(ListAPIView):
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAuthenticated, ]
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
