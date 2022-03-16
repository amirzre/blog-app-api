from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, phone, **extra_fields):
        """Creates and saves a new user"""
        if not phone:
            raise ValueError('The given phone must be set!')

        user = self.model(phone=phone, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_user(self, phone, **extra_fields):
        """Creates and saves a new user"""
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(phone, **extra_fields)

    def create_superuser(self, phone, **extra_fields):
        """Creates and saves a new super user"""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(phone, **extra_fields)
