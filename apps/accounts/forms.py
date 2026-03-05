from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "dob",
            "course",
            "year",
            "department",
            "college",
            "phone",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower()
        user.username = email  # keep default auth working
        user.email = email
        user.is_active = True
        user.is_verified = False
        if commit:
            user.save()
        return user


class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        email = (cleaned.get("email") or "").strip().lower()
        password = cleaned.get("password") or ""

        if not email or not password:
            return cleaned

        user = authenticate(username=email, password=password)
        if user is None:
            raise ValidationError("Invalid email or password.")

        if not user.is_active:
            raise ValidationError("Your account is disabled. Please contact support.")

        cleaned["user"] = user
        return cleaned