from celery import shared_task
from habits.services import send_telegram_notification
from django.utils import timezone
from .models import Habit, User
from datetime import datetime, timedelta

PERIOD_MAP = {
    "every day": 1,
    "every other day": 2,
    "every three days": 3,
    "every four days": 4,
    "every five days": 5,
    "every six days": 6,
    "every week": 7,
}


@shared_task
def check_habits_and_notify():
    """Проверяет активные привычки и отправляет уведомления."""
    now = timezone.localtime()
    current_time = now.time()
    current_date = now.date()

    time_window_start = (datetime.combine(current_date, current_time) - timedelta(minutes=5)).time()
    time_window_end = (datetime.combine(current_date, current_time) + timedelta(minutes=5)).time()

    habits = Habit.objects.filter(is_active=True, time__gte=time_window_start, time__lte=time_window_end)

    for habit in habits:

        last_activity_date = habit.updated_at.date() if habit.updated_at else habit.created_at.date()
        days_passed = (current_date - last_activity_date).days

        period_days = PERIOD_MAP.get(habit.period)

        if period_days is None:
            continue

        if days_passed % period_days == 0:
            user = habit.user
            chat_id = user.tg_chat_id

            if not chat_id:
                continue

            message = f"Напоминание: {habit.action} время {habit.time.strftime('%H:%M')} - {habit.place}"
            if habit.reward:
                message += f". Награда: {habit.reward}"
            elif habit.linked_habit:
                message += f". Награда: {habit.linked_habit.action}"

            try:
                send_telegram_notification(chat_id, message)
            except Exception as e:
                print(f"[ERROR] Ошибка при отправке в Telegram: {e}")
