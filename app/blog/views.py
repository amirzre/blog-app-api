from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog.serializers import (
    ListBlogsSerializer,
    CreateBlogSerializer,
    DetailUpdateDeleteBlogSerializer,
    ListCategorySerializer,

)
from blog.pagination import LimitOffsetPaginationBlog
from core.models import Blog, Category
from permissions import IsSuperUserOrAuthor, IsSuperUserOrAuthorOrReadOnly


class ListBlogApiView(ListAPIView):
    """Returns a list of all existing blogs"""

    serializer_class = ListBlogsSerializer
    pagination_class = LimitOffsetPaginationBlog
    filterset_fields = ('category', 'special')
    search_fields = ('title', 'summery', 'author__first_name')
    ordering_fields = ('publish', 'special')

    def get_queryset(self):
        return Blog.objects.publish()


class CreateBlogApiView(CreateAPIView):
    """Creates a new post instance"""

    serializer_class = CreateBlogSerializer
    permission_classes = (IsSuperUserOrAuthor,)

    def get_queryset(self):
        return Blog.objects.publish()

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            return serializer.save(
                author=self.request.user,
                status='d',
                special=False,
            )

        return serializer.save(author=self.request.user)


class DetailUpdateDeleteBlogApiView(RetrieveUpdateDestroyAPIView):
    """Returns the details of a post, Updates and Delete an existing post"""

    serializer_class = DetailUpdateDeleteBlogSerializer
    permission_classes = (IsSuperUserOrAuthorOrReadOnly,)
    lookup_field = 'slug'

    def get_object(self):
        blog = get_object_or_404(Blog, slug=self.kwargs.get('slug'))
        return blog

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            return serializer.save(
                author=self.request.user,
                status='d',
                special=False,
            )

        return serializer.save()


class CategoryBlogApiView(ListAPIView):
    """Returns the list of blogs on a particular category"""

    serializer_class = ListBlogsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        category = get_object_or_404(
                Category.objects.active(),
                slug=self.kwargs.get('slug')
            )
        queryset = category.blogs.publish()
        return queryset


class ListCategoryApiView(ListAPIView):
    """Returns a list of all existing category"""

    serializer_class = ListCategorySerializer
    lookup_field = 'slug'
    queryset = Category.objects.active()


class BlogLikeApiView(APIView):
    """Likes the desired blog"""

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        blog = get_object_or_404(Blog, pk=pk, status='p')

        if user in blog.likes.all():
            blog.likes.remove(user)
        else:
            blog.likes.add(user)

        return Response(
            {
                'Ok': 'Your request was successful.'
            },
            status=status.HTTP_200_OK,
        )
