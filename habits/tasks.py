from celery import shared_task
from habits.services import send_telegram_notification
from django.utils import timezone
from .models import Habit, User
from datetime import datetime, timedelta


@shared_task
def check_habits_and_notify():
    """Проверяет активные привычки и отправляет уведомления.

    Проверяет все активные привычки, у которых текущее время соответствует времени выполнения
    и периодичность совпадает с текущей датой.
    """
    now = timezone.now()
    current_time = now.time()
    current_date = now.date()

    time_window_start = (datetime.combine(current_date, current_time) - timedelta(minutes=5)).time()
    time_window_end = (datetime.combine(current_date, current_time) + timedelta(minutes=5)).time()

    habits = Habit.objects.filter(is_active=True, time__gte=time_window_start, time__lte=time_window_end)

    for habit in habits:
        last_notification = habit.updated_at.date() if habit.updated_at else habit.created_at.date()
        days_since_last = (current_date - last_notification).days

        if days_since_last % habit.period == 0:
            try:
                user_profile = habit.user.profile
                chat_id = user_profile.telegram_chat_id
                if chat_id:
                    message = f"Напоминание: {habit.action} в {habit.time} в {habit.place}"
                    if habit.reward:
                        message += f". Награда: {habit.reward}"
                    elif habit.linked_habit:
                        message += f". Награда: {habit.linked_habit.action}"
                    send_telegram_notification.delay(chat_id, message)
            except User.DoesNotExist:
                continue
