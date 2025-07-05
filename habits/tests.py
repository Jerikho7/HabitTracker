from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.tasks import check_habits_and_notify
from unittest.mock import patch
from habits.services import send_telegram_notification

User = get_user_model()


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass123")
        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            "action": "Пробежка",
            "place": "Парк",
            "time": "07:00:00",
            "period": "every day",
            "reward": "Мороженое",
            "execution_time": 30,
            "is_pleasant": False,
            "is_public": True,
        }

    def test_create_habit(self):
        url = reverse("habits:habits-list")
        response = self.client.post(url, self.habit_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().action, "Пробежка")

    def test_list_user_habits(self):
        Habit.objects.create(user=self.user, **self.habit_data)
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_habit(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        url = reverse("habits:habits-detail", kwargs={"pk": habit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Пробежка")

    def test_update_habit(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        url = reverse("habits:habits-detail", kwargs={"pk": habit.pk})
        updated_data = self.habit_data.copy()
        updated_data["action"] = "Йога"
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "Йога")

    def test_soft_delete_habit(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        url = reverse("habits:habits-detail", kwargs={"pk": habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        habit.refresh_from_db()
        self.assertFalse(habit.is_active)

    def test_check_habits_runs(self):
        result = check_habits_and_notify.apply()
        assert result.successful()

    @patch("habits.services.requests.get")
    def test_send_telegram_notification(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "ok"
        send_telegram_notification("123456", "Test")
        mock_get.assert_called_once()
