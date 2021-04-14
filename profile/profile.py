from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


def change_profile_data():
    pass


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
