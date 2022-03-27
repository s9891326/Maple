from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagersTests(TestCase):
    def setUp(self) -> None:
        self.User = get_user_model()
        self.username = "eddy"
        self.user_email = "eddy@google.com"
        self.user_password = "eddy"
        
        self.superuser_name = "root"
        self.superuser_email = "root@google.com"
        self.superuser_password = "root_password"
    
    def test_create_user(self):
        user = self.User.objects.create_user(
            username=self.username,
            email=self.user_email,
            password=self.user_password
        )
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.user_email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='')

    def test_create_superuser(self):
        superuser = self.User.objects.create_superuser(
            username=self.superuser_name,
            email=self.superuser_email,
            password=self.superuser_password
        )
        self.assertEqual(superuser.username, self.superuser_name)
        self.assertEqual(superuser.email, self.superuser_email)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                username="test_root",
                email="root@google.com",
                password="root",
                is_superuser=False
            )
