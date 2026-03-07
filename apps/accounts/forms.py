from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class SignUpStep1Form(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    dob = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email


class SignUpStep2Form(forms.Form):
    college = forms.CharField(max_length=255)
    course = forms.CharField(max_length=150)
    year = forms.ChoiceField(choices=User.YEAR_CHOICES)
    cgpa = forms.DecimalField(
    max_digits=4,
    decimal_places=2,
    widget=forms.NumberInput(attrs={
        "step": "0.01",
        "min": "0",
        "max": "10",
        "placeholder": "e.g. 8.75",
        "class": "w-full"
    })
)


class SignUpStep3Form(UserCreationForm):
    class Meta:
        model = User
        fields = ("password1", "password2")


class SignUpStep4Form(forms.Form):
    preferred_category = forms.ChoiceField(
        choices=User.PREFERRED_CATEGORY_CHOICES
    )
    interested_fields = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    preferred_location = forms.ChoiceField(
        choices=User.PREFERRED_LOCATION_CHOICES
    )
    skills = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )


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