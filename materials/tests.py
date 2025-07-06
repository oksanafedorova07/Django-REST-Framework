from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson, Subscription

User = get_user_model()


class CourseCRUDTestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем тестовый курс
        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание тестового курса",
            owner=self.user,
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            description="Описание тестового урока",
            video_url="https://www.youtube.com/watch?v=test",
            course=self.course,
            owner=self.user,
        )

    def test_create_course(self):
        """Тест создания курса"""
        url = reverse("course-list")
        data = {"name": "Новый курс", "description": "Описание нового курса"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(response.data["name"], "Новый курс")

    def test_list_courses(self):
        """Тест получения списка курсов"""
        url = reverse("course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_course(self):
        """Тест получения конкретного курса"""
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый курс")

    def test_update_course(self):
        """Тест обновления курса"""
        url = reverse("course-detail", args=[self.course.id])
        data = {"name": "Обновленный курс", "description": "Обновленное описание"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Обновленный курс")

    def test_delete_course(self):
        """Тест удаления курса"""
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_create_lesson(self):
        """Тест создания урока"""
        url = reverse("lesson-list-create")
        data = {
            "name": "Новый урок",
            "description": "Описание нового урока",
            "video_url": "https://www.youtube.com/watch?v=new",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_list_lessons(self):
        """Тест получения списка уроков"""
        url = reverse("lesson-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_lesson(self):
        """Тест получения конкретного урока"""
        url = reverse("lesson-detail", args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый урок")

    def test_update_lesson(self):
        """Тест обновления урока"""
        url = reverse("lesson-detail", args=[self.lesson.id])
        data = {
            "name": "Обновленный урок",
            "description": "Обновленное описание урока",
            "video_url": "https://www.youtube.com/watch?v=updated",
            "course": self.course.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновленный урок")

    def test_delete_lesson(self):
        """Тест удаления урока"""
        url = reverse("lesson-detail", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        self.client.force_authenticate(user=None)
        url = reverse("course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_foreign_user_access(self):
        """Тест доступа другого пользователя к чужим курсам"""
        other_user = User.objects.create_user(
            email="other@example.com", password="otherpass123"
        )
        self.client.force_authenticate(user=other_user)
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем тестовый курс
        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание тестового курса",
            owner=self.user,
        )

    def test_create_subscription(self):
        """Тест создания подписки"""
        url = reverse("subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_remove_subscription(self):
        """Тест удаления подписки"""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_status_in_course(self):
        """Тест отображения статуса подписки в курсе"""
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    def test_no_subscription_status_in_course(self):
        """Тест отображения отсутствия подписки в курсе"""
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])

    def test_subscription_unauthorized(self):
        """Тест подписки без авторизации"""
        self.client.force_authenticate(user=None)
        url = reverse("subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VideoURLValidatorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание тестового курса",
            owner=self.user,
        )

    def test_valid_youtube_url(self):
        """Тест валидной ссылки на YouTube"""
        url = reverse("lesson-list-create")
        data = {
            "name": "Урок с YouTube",
            "description": "Описание урока",
            "video_url": "https://www.youtube.com/watch?v=valid",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_external_url(self):
        """Тест невалидной внешней ссылки"""
        url = reverse("lesson-list-create")
        data = {
            "name": "Урок с внешней ссылкой",
            "description": "Описание урока",
            "video_url": "https://example.com/video",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Разрешены только ссылки на YouTube", str(response.data))

    def test_invalid_educational_platform_url(self):
        """Тест невалидной ссылки на образовательную платформу"""
        url = reverse("lesson-list-create")
        data = {
            "name": "Урок с образовательной платформы",
            "description": "Описание урока",
            "video_url": "https://coursera.org/lesson",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Разрешены только ссылки на YouTube", str(response.data))
