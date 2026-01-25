import datetime

from django import forms
from django_filters import FilterSet, filters
from .models import Post


class NewsFilter(FilterSet):
    created_at = filters.DateFilter(method='filter_created_after_date', widget=forms.DateInput(attrs={'type': 'date'}))

    def filter_created_after_date(self, queryset, name, value):
        if value:
            next_day = value + datetime.timedelta(days=1)
            return queryset.filter(created_at__gte=next_day)
        return queryset

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user__username': ['icontains'],
        }
