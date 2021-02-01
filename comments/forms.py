from django import forms

from .models import ProductComment


class ProductCommentForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=ProductComment.RATING_CHOICES)

    class Meta:
        model = ProductComment
        fields = ('rating', 'description',)
