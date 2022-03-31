from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone:
            raise ValueError('The given phone must be set!')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):
        """Creates and saves a new super user"""
        user = self.create_user(phone, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class BlogManager(Manager):

    def publish(self):
        """Return all published blogs"""
        return self.filter(status='p')


class CategoryManager(Manager):

    def active(self):
        """Return active categories"""
        return self.filter(status=True)
