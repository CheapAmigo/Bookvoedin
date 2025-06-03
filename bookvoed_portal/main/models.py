from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    full_name = models.CharField(
        max_length=100, 
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё\s]+$', 
                message="ФИО должно содержать только кириллицу и пробелы."
            )
        ],
        verbose_name='ФИО'
    )
    phone = models.CharField(
        max_length=12, 
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$', 
                message="Формат +7XXXXXXXXXX"
            )
        ],
        verbose_name='Телефон'
    )
    email = models.EmailField(unique=True, verbose_name='Email')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class BookCard(models.Model):
    BINDING_CHOICES = [
        ('твердый', 'Твердый'),
        ('мягкий', 'Мягкий'),
    ]
    
    CONDITION_CHOICES = [
        ('идеальное', 'Идеальное'),
        ('нормальное', 'Нормальное'),
        ('требует внимания', 'Требует внимания'),
        ('плохое', 'Годится чтобы подпирать ножку стола'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('archived', 'В архиве'),
    ]
    
    TYPE_CHOICES = [
        ('share', 'Готов поделиться'),
        ('want', 'Хочу в свою библиотеку'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, verbose_name='Автор')
    title = models.CharField(max_length=100, verbose_name='Название')
    book_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Тип карточки')
    publisher = models.CharField(max_length=100, blank=True, verbose_name='Издательство')
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год издания')
    binding = models.CharField(max_length=10, choices=BINDING_CHOICES, blank=True, verbose_name='Переплет')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, verbose_name='Состояние')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    rejection_reason = models.TextField(blank=True, verbose_name='Причина отклонения')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.status == 'rejected' and not self.rejection_reason:
            raise ValidationError(
                {'rejection_reason': 'При отклонении необходимо указать причину'}
            )
        
        # Очищаем причину, если статус не "Отклонено"
        if self.status != 'rejected':
            self.rejection_reason = ''
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Вызывает clean() перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Карточка книги'
        verbose_name_plural = 'Карточки книг'
    
    def __str__(self):
        return f"{self.author} - {self.title} ({self.get_book_type_display()})"