from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    """Пагинатор для привычек - 5 элементов на страницу."""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100
