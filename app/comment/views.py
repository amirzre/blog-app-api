from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from comment.serializers import (
    ListCommentSerializer,
    CreateUpdateCommentSerializer
)
from core.models import Blog, Comment


class ListCommentApiView(APIView):
    """Returns the list of comments on a particular post"""

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk, status="p")
        query = Comment.objects.filter_by_instance(blog)
        serializer = ListCommentSerializer(query, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CreateCommentApiView(APIView):
    """Create a comment instnace and returns created comment data"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CreateUpdateCommentSerializer(data=request.data)

        if serializer.is_valid():
            blog = get_object_or_404(
                Blog, pk=serializer.data.get('object_id'), status='p'
            )
            comment_for_model = ContentType.objects.get_for_model(blog)
            Comment.objects.create(
                user=request.user,
                name=serializer.data.get('name'),
                content_type=comment_for_model,
                object_id=blog.id,
                parent_id=serializer.data.get('parent'),
                body=serializer.data.get('body')
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateDeleteCommentApiView(APIView):
    """Updates and delete an existing comment"""

    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        serializer = CreateUpdateCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        return Response(status.HTTP_204_NO_CONTENT,)
