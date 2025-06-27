from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from users.permissions import IsModer, IsOwnerOrReadOnly

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course. Разграничение прав:
    - Создание и удаление запрещено для модераторов
    - Редактирование разрешено модераторам и владельцам
    - Просмотр списка доступен всем
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Настройка прав доступа по action-методам"""
        if self.action in ["create", "destroy"]:
            self.permission_classes = [~IsModer]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsModer | IsOwnerOrReadOnly]
        elif self.action == "list":
            self.permission_classes = []  # Открытый доступ к списку

        return super().get_permissions()

    def perform_create(self, serializer):
        """Автоматически привязываем владельца при создании курса"""
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    """Получение списка уроков и создание нового урока
    - Создание запрещено для модераторов
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """Ограничиваем возможность создания уроков для модераторов"""
        if self.request.method == "POST":
            self.permission_classes = [~IsModer]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Привязываем владельца при создании урока"""
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.GenericAPIView):
    """Обработка GET, PUT, DELETE для одного урока через GenericAPIView"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_object(self):
        return super().get_object()

    def get(self, request, *args, **kwargs):
        lesson = self.get_object()
        serializer = self.get_serializer(lesson)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        lesson = self.get_object()
        serializer = self.get_serializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        lesson = self.get_object()
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    """Доступ только аутентифицированным пользователям, которые являются владельцами"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    """Доступ только аутентифицированным пользователям, которые являются владельцами"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
