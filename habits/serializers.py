from rest_framework import serializers
from .models import Habit
from .validators import (
    RewardOrRelatedValidator,
    ExecutionTimeValidator,
    PleasantRelatedValidator,
    PleasantHabitValidator,
    PeriodStringValidator,
    RelatedPublicValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit с внешними валидаторами."""

    linked_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "linked_habit",
            "period",
            "reward",
            "execution_time",
            "is_public",
        )
        validators = [
            RewardOrRelatedValidator("linked_habit", "reward"),
            ExecutionTimeValidator("execution_time"),
            PleasantRelatedValidator("linked_habit"),
            PleasantHabitValidator("is_pleasant", "reward", "linked_habit"),
            PeriodStringValidator("period"),
            RelatedPublicValidator("linked_habit", "is_public"),
        ]
        extra_kwargs = {"user": {"read_only": True}}


class PublicHabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = ("action", "period", "time")
