from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import display
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.managers import (
    UserManager,
    BlogManager,
    CategoryManager,
    CommentManager
)
from extensions.upload_file_path import upload_file_path


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using phone instead of username"""

    phone_regex = RegexValidator(
        regex=r"^989\d{2}\s*?\d{3}\s*?\d{4}$",
        message=_("Invalid phone number.")
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], unique=True,
        verbose_name=_("phone")
    )
    first_name = models.CharField(
        max_length=100, blank=True, verbose_name=_('first name')
    )
    last_name = models.CharField(
        max_length=100, blank=True, verbose_name=_('last name')
    )
    author = models.BooleanField(
        default=False, blank=True, verbose_name=_('author')
    )
    special_user = models.DateTimeField(
        default=timezone.now, verbose_name=_('Special User')
    )
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_('date joined')
    )
    two_step_password = models.BooleanField(
        default=False, verbose_name=_('two step password'),
        help_text=_("is active two step password?"),
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    @property
    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    @display(
        boolean=True,
        description=_('Special User')
    )
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False


class PhoneOtp(models.Model):
    """Otp code that send for phone number"""

    phone_regex = RegexValidator(
        regex=r"^989\d{2}\s*?\d{3}\s*?\d{4}$",
        message=_("Invalid phone number."),
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], unique=True,
        verbose_name=_("phone"),
    )
    otp = models.CharField(max_length=6)

    count = models.PositiveSmallIntegerField(
        default=0, help_text=_("Number of otp sent")
    )
    verify = models.BooleanField(default=False, verbose_name=_("is verify"))

    def __str__(self):
        return self.phone


class Blog(models.Model):
    """Model for create new blog"""

    STATUS_CHOICES = (
        ('p', 'publish'),
        ('d', 'draft'),
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='blogs',
        default=None,
        blank=False,
        null=False,
        verbose_name=_('Author')
    )
    category = models.ManyToManyField(
        'Category',
        default=None,
        related_name='blogs',
        blank=True,
        verbose_name=_('Categories')
    )
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name=_('Slug')
    )
    body = models.TextField(blank=False, verbose_name=_("Content"))
    image = models.ImageField(
        upload_to=upload_file_path,
        verbose_name=_('Image')
    )
    summery = models.TextField(max_length=400, verbose_name=_('Summery'))
    likes = models.ManyToManyField(
        get_user_model(),
        related_name='blogs_like',
        blank=True,
        verbose_name=_('Likes')
    )
    publish = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Publish Time')
    )
    create = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Create Time')
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Update Time')
    )
    special = models.BooleanField(
        default=False,
        verbose_name=_('Is special blog?')
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        verbose_name=_('Status')
    )
    visits = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Visits')
    )

    objects = BlogManager()

    def __str__(self):
        return f'{self.author.first_name} - {self.title}'

    class Meta:
        ordering = ('-publish', '-updated')
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')


class Category(models.Model):
    """Model for create new category"""

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        default=None,
        blank=True,
        null=True,
        verbose_name=_('SubCategory')
    )
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name=_('Slug')
    )
    status = models.BooleanField(default=False, verbose_name=_('Status'))

    objects = CategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Comment(models.Model):
    """Model for create new comment"""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('User')
    )
    name = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('Name')
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name=_('Comments')
    )
    object_id = models.PositiveIntegerField(verbose_name=_('object_id'))
    content_object = GenericForeignKey("content_type", "object_id")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
        verbose_name=_('Parent')
    )
    body = models.TextField(verbose_name=_("Body"))
    create = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Create time")
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Update time")
    )

    objects = CommentManager()

    def __str__(self):
        return self.user.phone

    class Meta:
        ordering = ('-create', '-id')
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
