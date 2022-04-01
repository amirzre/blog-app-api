from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetPaginationBlog(LimitOffsetPagination):
    """Pagination for blog page"""

    default_limit = 20
    max_limit = 20
