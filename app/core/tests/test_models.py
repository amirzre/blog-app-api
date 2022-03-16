from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_phone_successful(self):
        """Test creating new user with an phone is successful"""
        phone = '989361234567'
        user = get_user_model().objects.create_user(
            phone=phone,
        )

        self.assertEqual(user.phone, phone)

    def test_new_user_invalid_phone(self):
        """Test creating user with no phone raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None)

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            phone='989361234567'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
