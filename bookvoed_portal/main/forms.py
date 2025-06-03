from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import User, BookCard
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        min_length=6,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё\w]+$',
                message='Логин должен содержать только кириллицу, латиницу и цифры'
            )
        ],
        help_text='Минимум 6 символов'
    )
    

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'phone', 'email']
        labels = {
            'full_name': 'ФИО',
            'phone': 'Телефон',
            'email': 'Email',
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class BookCardForm(forms.ModelForm):
    class Meta:
        model = BookCard
        fields = ['author', 'title', 'book_type', 'publisher', 'year', 'binding', 'condition']
        labels = {
            'author': 'Автор',
            'title': 'Название',
            'book_type': 'Тип карточки',
            'publisher': 'Издательство',
            'year': 'Год издания',
            'binding': 'Переплет',
            'condition': 'Состояние',
        }
        widgets = {
            'book_type': forms.RadioSelect(),
        }