from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Subscription
from .permissions import IsOwnerOrModerator
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .paginators import CoursePagination, LessonPagination


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.none()
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsOwnerOrModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsOwnerOrModerator]
        return super().get_permissions()

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.none()
    pagination_class = LessonPagination

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        
        subscription = Subscription.objects.filter(user=user, course=course)
        
        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
        
        return Response({"message": message})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    queryset = Lesson.objects.none()

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)
