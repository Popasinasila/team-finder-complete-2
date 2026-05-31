from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    """Form for new user registration."""

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Фамилия"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Email",
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Form for user login with email + password."""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio", "phone", "github", "avatar"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Фамилия"}),
            "bio": forms.Textarea(attrs={"placeholder": "О себе", "rows": 3}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 (000) 000-00-00"}),
            "github": forms.URLInput(attrs={"placeholder": "https://github.com/username"}),
        }
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "bio": "О себе",
            "phone": "Телефон",
            "github": "GitHub",
            "avatar": "Аватар",
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """Styled password change form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(
            attrs={"placeholder": "Текущий пароль"}
        )
        self.fields["new_password1"].widget = forms.PasswordInput(
            attrs={"placeholder": "Новый пароль"}
        )
        self.fields["new_password2"].widget = forms.PasswordInput(
            attrs={"placeholder": "Повторите новый пароль"}
        )
        self.fields["old_password"].label = "Текущий пароль"
        self.fields["new_password1"].label = "Новый пароль"
        self.fields["new_password2"].label = "Подтверждение нового пароля"
