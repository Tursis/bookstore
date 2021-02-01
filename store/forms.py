from django import forms
from .models import Book, Magazine


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = '__all__'


