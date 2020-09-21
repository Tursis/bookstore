from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class AuthCheckerMixin(UserPassesTestMixin):
    login_url = 'login'
    redirect_field_name = 'registration/login.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True

    def handle_no_permission(self):
        return redirect('store:index')
