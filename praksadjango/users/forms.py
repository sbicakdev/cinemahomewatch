from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinValueValidator, MaxValueValidator


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords do not match!")
            
            try:
                validate_password(password1)
            except ValidationError as e:
                self.add_error('password1', e) 

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists!")
        return username

    def registeruser(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150,label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")




