from rest_framework.exceptions import ValidationError


class RewardOrRelatedValidator:
    """Нельзя одновременно указывать вознаграждение и связанную привычку."""

    def __init__(self, linked_field, reward_field):
        self.linked_field = linked_field
        self.reward_field = reward_field

    def __call__(self, attrs):
        if attrs.get(self.reward_field) and attrs.get(self.linked_field):
            raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")


class PleasantHabitValidator:
    """Приятная привычка не может иметь вознаграждение или связанную привычку."""

    def __init__(self, pleasant_field, reward_field, linked_field):
        self.pleasant_field = pleasant_field
        self.reward_field = reward_field
        self.linked_field = linked_field

    def __call__(self, attrs):
        if attrs.get(self.pleasant_field) and (attrs.get(self.reward_field) or attrs.get(self.linked_field)):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")


class ExecutionTimeValidator:
    """Время выполнения не должно превышать 120 секунд."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value and value > 120:
            raise ValidationError({self.field: "Время выполнения не должно превышать 120 секунд."})


class PleasantRelatedValidator:
    """Связанной может быть только приятная привычка."""

    def __init__(self, linked_field):
        self.linked_field = linked_field

    def __call__(self, attrs):
        linked = attrs.get(self.linked_field)
        if linked and not linked.is_pleasant:
            raise ValidationError({self.linked_field: "Связанной может быть только приятная привычка."})


class PeriodStringValidator:
    """Проверка: привычка не должна быть реже, чем раз в неделю."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        period = attrs.get(self.field)
        if period is None:
            return

        TOO_RARE_VALUES = [
            "every week",
        ]

        if period in TOO_RARE_VALUES:
            raise ValidationError({self.field: "Привычка должна выполняться хотя бы раз в неделю, но не реже."})


class RelatedPublicValidator:
    """Если привычка публичная, то и связанная должна быть публичной."""

    def __init__(self, linked_field, public_field):
        self.linked_field = linked_field
        self.public_field = public_field

    def __call__(self, attrs):
        linked = attrs.get(self.linked_field)
        is_public = attrs.get(self.public_field)
        if linked and is_public and not linked.is_public:
            raise ValidationError("Публичная привычка не может ссылаться на приватную связанную привычку.")
