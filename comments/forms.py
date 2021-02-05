from django import forms

from .models import ProductReviews, ReviewComment


class ProductReviewsForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=ProductReviews.RATING_CHOICES)

    class Meta:
        model = ProductReviews
        fields = ('rating', 'description',)


class ReviewCommentForm(forms.ModelForm):

    class Meta:
        model = ReviewComment
        fields = ('comment',)
