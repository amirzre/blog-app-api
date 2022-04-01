from rest_framework import serializers

from core.models import Comment


class ListCommentSerializer(serializers.ModelSerializer):
    """List all comments"""

    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('user', 'name', 'parent', 'body', 'create', 'object_id')

    def get_user(self, obj):
        return {
            "name": obj.user.first_name,
        }


class CreateUpdateCommentSerializer(serializers.ModelSerializer):
    """Creates and updates comments"""

    class Meta:
        model = Comment
        fields = ('object_id', 'name', 'parent', 'body')
