import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Создает тестовые данные для модели Payment"

    def create_groups(self):
        groups = ['moderators', 'students']
        for group in groups:
            Group.objects.get_or_create(name=group)
            self.stdout.write(self.style.SUCCESS(f'Создана группа: {group}'))

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаем добавление данных...")

        # Создаем группы если их нет
        self.create_groups()

        # Создаем тестового пользователя если нет
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'is_staff': False,
                'is_active': True
            }
        )
        if created:
            user.set_password('12345')  # Устанавливаем пароль
            user.save()
            self.stdout.write(self.style.SUCCESS('Создан тестовый пользователь'))

        # Создаем тестовый курс если нет
        course, c_created = Course.objects.get_or_create(
            name='Тестовый курс',
            defaults={
                'description': 'Описание тестового курса',
                'owner': user
            }
        )
        if c_created:
            self.stdout.write(self.style.SUCCESS('Создан тестовый курс'))

        # Создаем тестовый урок если нет
        lesson, l_created = Lesson.objects.get_or_create(
            name='Тестовый урок',
            course=course,
            defaults={
                'description': 'Описание тестового урока',
                'owner': user,
                'video_url': 'https://youtube.com/test'
            }
        )
        if l_created:
            self.stdout.write(self.style.SUCCESS('Создан тестовый урок'))

        # Создаем платежи
        payments = [
            {
                "user": user,
                "course": course,
                "lesson": None,
                "amount": Decimal("1000.00"),
                "method": "transfer",
                "payment_date": datetime.datetime.now()
            },
            {
                "user": user,
                "course": None,
                "lesson": lesson,
                "amount": Decimal("200.00"),
                "method": "cash",
                "payment_date": datetime.datetime.now()
            },
        ]

        for data in payments:
            payment, created = Payment.objects.get_or_create(**data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан платеж: {payment.id}'))

        self.stdout.write(self.style.SUCCESS("Все данные успешно добавлены!"))
