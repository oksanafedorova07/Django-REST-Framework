from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentListView, UserProfileUpdateView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path(
        "profile/update/<int:pk>/", UserProfileUpdateView.as_view(), name="user-update"
    ),
    path("", include(router.urls)),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
]
