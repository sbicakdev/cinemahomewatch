from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        label="Rating",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = forms.CharField(label="Comment",max_length=300,widget=forms.Textarea)
    class Meta:
        model = Review
        fields = ['rating', 'comment']