from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from habits.models import Habit


class Command(BaseCommand):
    help = "Создает группу модераторов с правами на привычки"

    def handle(self, *args, **options):
        # Создаем или получаем группу
        mod_group, created = Group.objects.get_or_create(name="moderators")

        # Получаем ContentType для модели Habit
        habit_ct = ContentType.objects.get_for_model(Habit)

        # Получаем необходимые разрешения
        permissions = Permission.objects.filter(
            content_type=habit_ct, codename__in=["view_habit", "change_habit", "delete_habit"]
        )

        # Привязываем разрешения к группе
        mod_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Группа 'moderators' успешно создана с нужными правами"))
