from django import forms
from .models import Book, Magazine


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name',
                  'author',
                  'pages',
                  'publisher',
                  'pub_year',
                  'hard_cover',
                  'size',
                  'price',
                  'Discounts',
                  ]


class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = ['name',
                  'pages',
                  'publisher',
                  'pub_year',
                  'numb',
                  'numb_in_year'
                  'size',
                  'price',
                  'sub_price',
                  'Discounts',
                  ]
