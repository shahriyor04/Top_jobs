from django_filters import FilterSet, filters, CharFilter

from apps.models import Article, Vacancy, Resumes


class ArticleFilter(FilterSet):
    title = CharFilter(lookup_expr='title__icontains', )

    class Meta:
        model = Article
        fields = ['title', ]


class VacancyFilter(FilterSet):
    job = CharFilter(lookup_expr='job')
    company = CharFilter(lookup_expr='company')
    address = CharFilter(lookup_expr='address')

    class Meta:
        model = Vacancy
        fields = ['job', 'company', 'address']


class ResumeFilter(FilterSet):
    level = CharFilter(lookup_expr='level')
    job = CharFilter(lookup_expr='job')

    class Meta:
        model = Resumes
        fields = ['level', 'job']
