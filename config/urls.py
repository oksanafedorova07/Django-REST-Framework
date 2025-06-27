from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib import admin

from materials.views import CourseViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("materials.urls")),
    path("api/users/", include("users.urls")),
    path("api/", include("users.urls")),
]
