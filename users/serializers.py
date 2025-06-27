from rest_framework import serializers

from materials.serializers import CourseSerializer, LessonSerializer

from .models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "payment_date", "course", "lesson", "amount", "method"]
