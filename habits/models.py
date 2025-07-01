from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Habit(models.Model):
    """Модель привычки для трекера полезных привычек.

    Attributes:
        user (ForeignKey): Связь с пользователем, создавшим привычку.
        place (CharField): Место выполнения привычки.
        time (TimeField): Время выполнения привычки.
        action (CharField): Действие, которое представляет привычка.
        is_pleasant (BooleanField): Является ли привычка приятной.
        linked_habit (ForeignKey): Связанная приятная привычка как вознаграждение.
        period (CharField): Периодичность выполнения привычки.
        reward (CharField): Вознаграждение за выполнение привычки.
        execution_time (PositiveIntegerField): Время выполнения в секундах.
        is_public (BooleanField): Видна ли привычка другим пользователям.
        is_active (BooleanField): Активна ли привычка.
    """

    PERIOD_CHOICES = (
        (1, "каждый день"),
        (2, "через день"),
        (3, "раз в 3 дня"),
        (4, "раз в 4 дня"),
        (5, "раз в 5 дней"),
        (6, "раз в 6 дней"),
        (7, "раз в неделю"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="habits", verbose_name="user", help_text="Создатель привычки"
    )
    place = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Место выполнения привычки",
        help_text="Место, где выполняется привычка",
    )
    time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Время выполнения привычки",
        help_text="Укажите время, когда необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие привычки",
        help_text="Укажите действие, которое представляет собой привычка",
    )
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Приятная привычка", help_text="Указывает, является ли привычка приятной"
    )
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_pleasant": True},
        related_name="related_habits",
        verbose_name="Связанная привычка",
        help_text="Привычка-вознаграждение. Только приятные привычки",
    )
    period = models.CharField(
        choices=PERIOD_CHOICES,
        default=1,
        verbose_name="Периодичность выполнения",
        help_text="Периодичность в днях (1-7)",
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Вознаграждение за выполнение привычки",
    )
    execution_time = models.PositiveIntegerField(
        verbose_name="Время выполнения", help_text="Время выполнения в секундах (не более 120)"
    )
    is_public = models.BooleanField(
        default=False, verbose_name="Публичная", help_text="Доступна ли привычка для просмотра другими"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна", help_text="Указывает, активна ли привычка")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def clean(self):
        """Валидация данных привычки перед сохранением."""
        if self.reward and self.linked_habit:
            raise ValidationError("Нельзя одновременно указать вознаграждение и связанную привычку.")

        if self.execution_time > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")

        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError("Связанной может быть только приятная привычка.")

        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        if self.period < 1 or self.period > 7:
            raise ValidationError("Нельзя выполнять привычку реже одного раза в 7 дней.")

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    def delete(self, *args, **kwargs):
        """Переопределение метода удаления: пользователи деактивируют привычку, модераторы удаляют."""
        if kwargs.get("user") and kwargs["user"].is_staff:
            super().delete(*args, **kwargs)
        else:
            self.is_active = False
            self.save()

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
