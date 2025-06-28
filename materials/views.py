from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwnerOrModerator
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsOwnerOrModerator]
        elif self.action == 'destroy':
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

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    queryset = Lesson.objects.none()

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)
