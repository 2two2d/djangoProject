from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import UserManager
from datetime import datetime
from django.urls import reverse


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=50, help_text="ФИО")
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=254)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  # Идентификатор для обращения
    REQUIRED_FIELDS = ['email']  # Список имён полей для Superuser

    objects = UserManager()

    def __str__(self):
        return self.full_name

class Project(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    name = models.CharField(max_length=100, verbose_name='Project name')
    description = models.TextField(max_length=400, verbose_name='Description')
    img = models.ImageField(upload_to='img/', verbose_name='picture')
    apply_date = models.DateTimeField(default=datetime.now(), editable=False)
    author = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Project owner', null=True, blank=True, to_field='id')

    PROCESS_STATUS = (('i', 'In process'),
                      ('d', 'done'))

    TYPE_STATUS = (('f', '2D design'),
                   ('v', '3D design'),
                   ('s', 'Sketch'))

    process_status = models.CharField(
        max_length=1,
        choices=PROCESS_STATUS,
        blank=True,
        default='i',
        help_text='Status of project')

    type_status = models.CharField(
        max_length=1,
        choices=TYPE_STATUS,
        blank=True,
        default='f')

    def __str__(self):
        return self.name + f'(type - {self.type_status})'

    def delete(self, using=None, keep_parents=False):
        self.delete()

    def get_absolute_url(self):
        return reverse('profile_application_detail', args=[str(self.id)])



# Create your models here.


