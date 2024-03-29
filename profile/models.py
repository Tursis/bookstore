from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    """
    Модель профиля
    """
    BIRTH_YEAR_CHOICES = [x for x in range(1922, 2022)]
    BIRTH_MONTH_CHOICES = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня', 7: 'июля',
                           8: 'августа', 9: 'сентября',
                           10: 'октября', 11: 'ноября', 12: 'декабря'}

    BIRTH_DAY_CHOICES = [x for x in range(1, 32)]
    GENDER_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, verbose_name='Имя', help_text="Enter your name.", blank=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', help_text="Enter your last_name.", blank=True)
    surname = models.CharField(max_length=100, verbose_name='Отчество', help_text="Enter your surname.", blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='images/avatar/', verbose_name='Изображение', blank=True, null=True)


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=256, blank=True, null=True)
