from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_course_update_email(user_email, course_name, material_title):
    send_mail(
        subject=f'Обновление в курсе {course_name}',
        message=f'В курсе "{course_name}" появился новый материал: {material_title}',
        from_email='noreply@example.com',  # замените на ваш email
        recipient_list=[user_email],
    ) 