from django import forms
from django.forms import TextInput
from .models import Order


class OrderCreateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(OrderCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].initial = 'hello'

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
