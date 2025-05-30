from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    fixtures = ['socialapp.json']
    def setUp(self):
        self.data = {
            "first_name": "Kostya",
            "last_name": "Zaitsev",
            "username": 'kostyanx2',
            "email": "awopihaqopi@gmail.com",
            "password1": "12345678pP",
            "password2": "12345678pP",
        }
        self.path = reverse('users:registration')
        self.username = self.data["username"]

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post(self):
        self.assertFalse(User.objects.filter(username=self.username).exists())

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(User.objects.filter(username=self.username).exists())

        email_verification = EmailVerification.objects.filter(user__username = self.username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        user = User.objects.create(username=self.username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Пользователь с таким именем уже существует.", html=True)