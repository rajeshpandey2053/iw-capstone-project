from django.urls import reverse
from django.contrib.auth import get_user_model

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.education import College, University, Faculty, Education
from accounts.api.serializers import EducationSerializer
from rest_framework.authtoken.models import Token

from accounts.api.tokens import account_activation_token

User = get_user_model()


class UserTests(APITestCase):
    """
    api test for registering user
    """

    def setUp(self):
        """
        setting up education as it is
        required while registering user
        """
        self.college = self.setup_college()
        self.university = self.setup_university()
        self.faculty = self.setup_faculty()
        self.url = reverse('account:user-register')
        self.login_url = reverse('account:user-login')
        self.education = EducationSerializer(self.setup_education()).data
        self.data = {
            "username": "testUser",
            "email": "testuser@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "1234",
            "confirm_password": "1234",
            "profile": {
                "user": 1,
                "contact_number": "9860476499",
                "address": "kapan",
                "education": self.education
            }
        }
        self.response = self.client.post(self.url, data=self.data, format='json')
        user = User.objects.get()
        user.is_active = True
        user.save()
        self.login_data = {
            "email": "testuser@gmail.com",
            "password": "1234"
        }

    def setup_education(self):
        return Education.objects.create(semester=1, year=2,
                                        college=self.college,
                                        faculty=self.faculty,
                                        university=self.university)

    @staticmethod
    def setup_college():
        return College.objects.create(
            college_name='Test College',
            college_short_form='TC'
        )

    @staticmethod
    def setup_university():
        return University.objects.create(
            university_name='Test Uni',
            uni_short_form='TU'
        )

    @staticmethod
    def setup_faculty():
        return Faculty.objects.create(
            faculty_name='Test Faculty',
            fac_short_form='TF'
        )

    def get_token(self):
        login_response = self.client.post(self.login_url, data=self.login_data, format="json")
        token = login_response.data['token']
        return token

    def test_user_register(self):
        """
        ensure that we can create new user with the respective
        profile and education detail
        """
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@gmail.com')

    def test_user_activation(self):
        """
        performing test whether the user activation is
        working or not
        """
        user = User.objects.get()
        response = self.client.get(reverse('accounts:user-activate',
                                           kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                                                   'token': account_activation_token.make_token(user)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        """
        perform test to get the detail about the currently logged
        in user
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.get_token())
        response = self.client.get(reverse("account:user-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('user').get('email'), "testuser@gmail.com")

    def test_user_update(self):
        """
        performing test to update the user detail
        :return:
        """
        update_data = {
            "username": "testnotUser",
            "email": "testnotuser@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "profile": {
                "user": 1,
                "contact_number": "9860476499",
                "address": "kapan",
                "education": self.education,
            },
        }
        # files = {'media': open('accounts/tests/1.png', 'rb')}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.get_token())
        response = self.client.put(reverse("account:user-update"), update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testnotUser")
        self.assertNotEqual(response.data['username'], "testUser")

    def test_user_login(self):
        """
        performing test whether the token is generated or not
        after successful login of user
        :return:
        """
        response = self.client.post(self.login_url, self.login_data, format="json")
        token = response.data.get('token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(Token.objects.get().key, token)

    def test_user_changepassword(self):
        """performing test to update the user detail"""

        changepassword_data = {
            "old_password": "1234",
            "new_password": "123456"
        }
        updatedlogin_data = {
            "email": "testuser@gmail.com",
            "password": "123456"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.get_token())
        response = self.client.patch(
            reverse("account:change-password"),
            changepassword_data,
            format="json"
        )

        # test if the response status after patch is ok or not
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test if user can login with new password
        response = self.client.post(self.login_url, updatedlogin_data, format="json")
        token = response.data.get('token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(Token.objects.get().key, token)
        # test if user can login with old password or not
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_user_resetpassword(self):
        """performing test to reset password"""

        data = {
            "email": "testuser@gmail.com"
        }
        response = self.client.post(reverse('account:request-reset-email'), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email="testuser@gmail.com")
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        relativeLink = reverse(
            'accounts:password-reset-confirm',
            kwargs={'uidb64': uidb64, 'token': token}
        )
        resetconfirm_response = self.client.get(reverse(
            'accounts:password-reset-confirm',
            kwargs={'uidb64': uidb64, 'token': token}
        ))

        self.assertEqual(resetconfirm_response.status_code, status.HTTP_200_OK)
        reset_data = {
            "uidb64": resetconfirm_response.data["uidb64"],
            "token": resetconfirm_response.data["token"],
            "password": "1234567"
        }
        resetcomplete_response = self.client.patch(reverse('account:password-reset-complete'), reset_data,
                                                   format="json")
        self.assertEqual(resetcomplete_response.status_code, status.HTTP_200_OK)
        # test if now user can login with new password
        updatedlogin_data = {
            "email": "testuser@gmail.com",
            "password": "1234567"
        }

        response = self.client.post(self.login_url, updatedlogin_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test if user can login with old password
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_get_followers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.get_token())
        response = self.client.get(reverse('accounts:user-follow-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_follow_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.get_token())
        user2 = User.objects.create_user(
            username='test2',
            password='1234',
            email="test2@gmail.com"
        )
        user1 = User.objects.get(id=1)
        data = {
            "follow_to": user1.id,
            "follow_by": user2.id
        }
        response = self.client.post(reverse('accounts:user-follow-detail'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_logout(self):
        """performing user logout test"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.get_token())
        response = self.client.delete(reverse('accounts:user-logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
