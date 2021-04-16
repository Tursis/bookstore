from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth.models import User


def change_profile_data(request):
    user = request.user
    new_name = request.POST.get("name")
    new_last_name = request.POST.get("last_name")
    new_surname = request.POST.get("middle_name")
    new_gender = request.POST.get("gender")
    new_birthday = request.POST.get("birthday")
    new_phone_number = request.POST.get("phone_number")
    user.first_name = new_name
    user.last_name = new_last_name
    user.profile.surname = new_surname
    user.profile.gender = new_gender
    user.profile.birthday = new_birthday
    user.save()


def change_profile_email(request):
    user = request.user
    new_email = request.POST.get("email")
    if User.objects.filter(email=new_email).exists() and user.email != new_email:
        raise ValueError('email уже занят')
    else:
        user.email = new_email
    user.save()


def change_password(request):
    user = request.user
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    repeat_new_password = request.POST.get("repeat_new_password")
    if check_password(old_password, request.user.password):
        if new_password == repeat_new_password:
            validate_password(new_password, user)
            user.set_password(new_password)
            user.save()
        else:
            raise exceptions.ValidationError('Пароли не равны')
    else:
        raise exceptions.ValidationError('Не правильный пароль')


def exceptions_profile(request, func):
    errors = {}

    try:
        func(request)
    except ValueError as e:
        errors[func.__name__] = list(e.messages)
    return errors