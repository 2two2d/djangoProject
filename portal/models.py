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


class Category(models.Model):
    type = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.type

class Project(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    name = models.CharField(max_length=100, verbose_name='Project name')
    description = models.TextField(max_length=400, verbose_name='Description')
    img = models.ImageField(upload_to='img/', verbose_name='picture', null=True)
    apply_date = models.DateTimeField(default=datetime.now(), editable=False)
    author = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Project owner', null=True, blank=True, to_field='id')
    com = models.CharField(max_length=400, verbose_name='Description', default='Этот проект ещё не принят в разработку!')
    category = models.ForeignKey(Category, to_field='type', help_text='Категория заявки', blank=False,
                                 on_delete=models.CASCADE)

    PROCESS_STATUS = (('i', 'В процессе'),
                      ('d', 'Готовые'),
                      ('n', 'Новые'))



    process_status = models.CharField(
        max_length=1,
        choices=PROCESS_STATUS,
        blank=True,
        default='n',
        help_text='Статус')

    def __str__(self):
        return self.name + f'(type - {self.type_status})'


    def get_absolute_url(self):
        return reverse('profile_application_detail', args=[str(self.id)])





