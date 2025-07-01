from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, PublicHabitListAPIView

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')

urlpatterns = [
    path('public-habits/', PublicHabitListAPIView.as_view(), name='public-habits'),
] + router.urls
