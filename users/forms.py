from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import EmailVerification, User
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        "placeholder": "Введите имя пользователя"}))
    password =  forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4",
        "placeholder": "Введите пароль"}))
    class Meta:
        model = User
        fields = ("username", "password")


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        "placeholder": "Введите имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        "placeholder": "Введите фамилию"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        "placeholder": "Введите имя пользователя"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        "placeholder": "Введите почту"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4",
        "placeholder": "Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4",
        "placeholder": "Подтвердите пароль"}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=commit)
        send_email_verification.delay(user.id)
        return user

class UserProfileFrom(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
    "class": "form-control py-4"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
    "class": "form-control py-4"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
    "class": "form-control py-4", "readonly": True}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control py-4", "readonly": True}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class":"custom-file-input"}), required=False)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'image')