from rest_framework.pagination import PageNumberPagination


class ListResultsSetPagination(PageNumberPagination):
    page_size: int = 10
    page_size_query_param: str = "page_size"
    max_page_size: int = 1000
