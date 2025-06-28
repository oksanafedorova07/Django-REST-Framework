from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import Payment, User
from .serializers import (PaymentSerializer, PrivateUserSerializer,
                          PublicUserSerializer, UserSerializer)


class UserProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # По умолчанию — свежие сверху


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':  # Разрешить регистрацию без авторизации
            return [AllowAny()]
        return super().get_permissions()


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return PrivateUserSerializer
        return super().get_serializer_class()
