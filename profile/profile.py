from datetime import datetime

from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth.models import User


def change_profile_data(request):
    user = request.user
    user.first_name = request.POST.get("name")
    user.last_name = request.POST.get("last_name")
    user.profile.surname = request.POST.get("middle_name")
    user.profile.gender = request.POST.get("gender")
    new_birth_day = request.POST.get("birth_day")
    new_birth_month = request.POST.get("birth_month")
    new_birth_year = request.POST.get("birth_year")
    new_phone_number = request.POST.get("phone_number")
    new_birth_date = new_birth_year + '-' + new_birth_month + '-' + new_birth_day
    user.profile.birthday = datetime.strptime(new_birth_date, "%Y-%m-%d").date()
    user.save()


def change_profile_email(request):
    user = request.user
    new_email = request.POST.get("email")
    if User.objects.filter(email=new_email).exists() and user.email != new_email:
        raise exceptions.ValidationError('email уже занят')
    else:
        user.email = new_email
    user.save()


def change_password(request):
    user = request.user
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    repeat_new_password = request.POST.get("repeat_new_password")
    if request.POST.get("old_password") != '':
        if check_password(old_password, request.user.password):
            if new_password == repeat_new_password:
                validate_password(new_password, user)
                user.set_password(new_password)
                user.save()
            else:
                raise exceptions.ValidationError('Пароли не равны')
        else:
            raise exceptions.ValidationError('Не правильный пароль')


