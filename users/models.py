from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Пользователь"
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        'materials.Course',  # Строковая ссылка
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс"
    )
    lesson = models.ForeignKey(
        'materials.Lesson',  # Строковая ссылка
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name="Способ оплаты",
        default='cash'  # Добавляем значение по умолчанию
    )

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_date})"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']