from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .pagination import HabitPaginator
from users.permissions import IsOwner, IsModerator

class HabitViewSet(ModelViewSet):
    """ViewSet для CRUD операций с привычками."""
    pagination_class = HabitPaginator
    serializer_class = HabitSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["retrieve", "update", "partial_update", "list"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """Фильтрация привычек по владельцу."""
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            return Habit.objects.filter(user=user, is_active=True)
        return Habit.objects.all()

    def perform_create(self, serializer):
        """Привязка пользователя к создаваемой привычке."""
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Переопределение удаления для не-модераторов."""
        if self.request.user.is_staff:
            instance.delete()
        else:
            instance.is_active = False
            instance.save()

class PublicHabitListAPIView(ListAPIView):
    """Контроллер для списка публичных привычек."""
    queryset = Habit.objects.filter(is_public=True, is_active=True)
    serializer_class = PublicHabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]
