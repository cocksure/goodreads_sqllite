from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={"username": 'jama',
                  "first_name": 'Jamshid',
                  "last_name": "Anorbekov",
                  "email": "jama@mail.ru",
                  "password": "somepassword"
            }
        )

        user = CustomUser.objects.get(username="jama")

        self.assertEquals(user.first_name, 'Jamshid')
        self.assertEquals(user.last_name, 'Anorbekov')
        self.assertEquals(user.email, 'jama@mail.ru')
        self.assertNotEquals(user.password, 'somepassword')
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data = {
                "first_name": "Jamshid",
                "last_name": "jama@gmail.ru"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEquals(user_count, 0)

        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={"username": 'jama',
                  "first_name": 'Jamshid',
                  "last_name": "Anorbekov",
                  "email": "invalid-email",
                  "password": "somepassword"
                  }
        )
        user_count = CustomUser.objects.count()

        self.assertEquals(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        # 1. Create user
        user = CustomUser.objects.create(username="jama", first_name="Jamshid")
        user.set_password("somepass")
        user.save()

        # 2. try to create another user with that same username
        response = self.client.post(
            reverse("users:register"),
            data={"username": 'jama',
                  "first_name": 'Jamshid',
                  "last_name": "Anorbekov",
                  "email": "invalid-email",
                  "password": "somepassword"
                  }
        )

        # 3. check that the second user was not created
        user_count = CustomUser.objects.count()
        self.assertEquals(user_count, 1)

        # 4. check that the form contains the error message
        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="jama", first_name="Jamshid", last_name="Anorbekov", email="jama@mail.com")
        self.user.set_password("somepass")
        self.user.save()

    def test_successful_login(self):

        self.client.post(
            reverse("users:login"),
            data={
                "username": "jama",
                "password": "somepass"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):

        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "somepass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "jama",
                "password": "wrong_-pass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):

        self.client.login(username="jama", password="somepass")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(username="jama", first_name="Jamshid", last_name="Anorbekov", email="jama@mail.com")

        user.set_password("somepass")
        user.save()

        self.client.login(username="jama", password="somepass")

        response = self.client.get((reverse("users:profile")))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(username="jama", first_name="Jamshid", last_name="Anorbekov", email="jama@mail.com")
        user.set_password("somepass")
        user.save()

        self.client.login(username="jama", password="somepass")

        response = self.client.post(
            reverse("users:profile_edit"),
            data={
                "username": "jama",
                "first_name": "Jamshid",
                "last_name": "Editov",
                "email": "something@gmail.com"
            }

        )
        user.refresh_from_db()

        self.assertEqual(user.last_name, "Editov")
        self.assertEqual(user.email, "something@gmail.com")

        self.assertEqual(response.url, reverse("users:profile"))
