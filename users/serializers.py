from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from materials.serializers import CourseSerializer, LessonSerializer
from .models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'email', 'password', "phone", "city", "avatar"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        # Хэширование пароля
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "payment_date", "course", "lesson", "amount", "method"]


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "city", "avatar"]


class PrivateUserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "payments"]
