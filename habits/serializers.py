from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit.

    Используется для отображения и валидации данных привычек.
    Включает только указанные поля: place, time, action, linked_habit, period, reward.
    """

    linked_habit = serializers.SlugRelatedField(
        slug_field='action',
        queryset=Habit.objects.filter(is_pleasant=True),
        allow_null=True
    )

    class Meta:
        model = Habit
        fields = ("place", "time", "action", "linked_habit", "period", "reward")

class PublicHabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = ("action", "period", "time")
