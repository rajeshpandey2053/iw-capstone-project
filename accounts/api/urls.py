from django.urls import path, include
from .views import (UserRegistrationView, 
                    UserDetail, 
                    UserUpdate, 
                    ChangePasswordView, 
                    PasswordTokenCheckAPI, 
                    RequestPasswordResetEmail, 
                    SetNewPasswordAPIView,UserRegistrationView, activate, UserLogoutView,
                    UserFollowAPIView, FacultyAPIView, UniversityAPIView
                    )
from .authtoken_views import CustomObtainAuthToken


user_url = [
    path('profile', UserDetail.as_view(), name='user-profile'),
    path('update', UserUpdate.as_view(), name = 'user-update'),
    path('activate/<uidb64>/<token>', activate, name='user-activate'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('request-reset-password/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('logout', UserLogoutView.as_view(), name='user-logout'),
    path('follow/detail', UserFollowAPIView.as_view(), name='user-follow-detail')
]


urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='user-register'),
    path('login', CustomObtainAuthToken.as_view(), name='user-login'),
    path('user/', include(user_url)),
    path('faculty', FacultyAPIView.as_view(), name='faculty'),
    path('university', UniversityAPIView.as_view(), name='university')
]
