from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)
    User.objects.filter(last_login__lt=month_ago, is_active=True).update(is_active=False) 