from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager
from django.db import models
from django.contrib.contenttypes.models import ContentType


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


class CommentManager(models.Manager):

    def filter_by_instance(self, instance):
        comment = ContentType.objects.get_for_model(instance)
        object_id = instance.id
        query = self.filter(content_type=comment, object_id=object_id)
        return query
