import django_filters

from Blog.models import Post


class PostFilter(django_filters.FilterSet):
    # title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    # author = django_filters.CharFilter(field_name="author", lookup_expr="icontains")

    class Meta:
        model = Post
        fields = ['title', 'author']
