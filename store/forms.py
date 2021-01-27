from django import forms
from .models import Book, Magazine, ProductComment


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = '__all__'


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('description',)
