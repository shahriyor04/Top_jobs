from django_filters import FilterSet, CharFilter

from direct_video.models import Direct_video


class DirectVideoFilter(FilterSet):
    category = CharFilter()
    title = CharFilter()

    class Meta:
        model = Direct_video
        fields = ['category', 'title']
