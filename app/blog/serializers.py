from rest_framework import serializers

from core.models import Blog, Category


class ListBlogsSerializer(serializers.ModelSerializer):
    """Return list all blogs"""

    author = serializers.SerializerMethodField(method_name='get_author')
    category = serializers.SerializerMethodField(method_name='get_category')

    class Meta:
        model = Blog
        fields = ('id', 'author', 'category', 'likes', 'create', 'body',
                  'status', 'updated', 'publish', 'visits', 'special')

    def get_author(self, obj):
        return {
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
        }

    def get_category(self, obj):
        category = [cat.title for cat in obj.category.get_queryset()]
        return category


class CreateBlogSerializer(serializers.ModelSerializer):
    """Create a new blog"""

    category = serializers.SlugRelatedField(
        many=True,
        slug_field='id',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Blog
        fields = ('id', 'title', 'body', 'image', 'summery', 'category',
                  'publish', 'special', 'status')


class DetailUpdateDeleteBlogSerializer(serializers.ModelSerializer):
    """get, update and delete blog"""

    author = serializers.SerializerMethodField(method_name='get_author')
    slug = serializers.ReadOnlyField()
    likes = serializers.SerializerMethodField(method_name='get_likes')

    class Meta:
        model = Blog
        exclude = ('create', 'updated')
        read_only_fields = ('likes',)

    def get_author(self, obj):
        return {
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
        }

    def get_likes(self, obj):
        return obj.likes.count()


class ListCategorySerializer(serializers.ModelSerializer):
    """Return list all category"""

    parent = serializers.SerializerMethodField(method_name='get_parent')

    class Meta:
        model = Category
        fields = ('parent', 'title')

    def get_parent(self, obj):
        return {
            'title': str(obj.parent),
        }
