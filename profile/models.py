from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    GENDER_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, verbose_name='Имя', help_text="Enter your name.", blank=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', help_text="Enter your last_name.", blank=True)
    surname = models.CharField(max_length=100, verbose_name='Отчество', help_text="Enter your surname.", blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='images/avatar/', verbose_name='Изображение', blank=True, null=True)
    token = models.CharField(max_length=256, blank=True, null=True)
