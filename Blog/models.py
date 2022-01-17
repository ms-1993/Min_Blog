from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
# Create your models here.
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('The email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """ custom user model """

    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.BigIntegerField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    def create_user(self):
        pass

    class Meta:
        verbose_name = 'User'
        ordering = ['-date_joined']


# from django.utils.text import slugify
from ckeditor.fields import RichTextField

User = get_user_model()


# each field in this class represents a column in the database table
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    Body = RichTextField()
    thumbnail = models.ImageField(upload_to='thumbnail', blank=True, null=True)
    posted_date_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # this class contains metadata and uses the created_on field from the model to sort out data which sorts
    # in descending order by default
    class Meta:
        ordering = ['-posted_date_on']

    # this method is the default human-readable representation of the object. Django will use it in many places
    # such as the admin panel
    def __str__(self):
        return str(self.title)
    #
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Post, self).save(*args, **kwargs)
