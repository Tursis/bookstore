from django import forms

from .models import ProductReviews


class ProductReviewsForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=ProductReviews.RATING_CHOICES)

    class Meta:
        model = ProductReviews
        fields = ('rating', 'description',)
