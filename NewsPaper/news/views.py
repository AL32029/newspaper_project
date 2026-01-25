from django.views.generic import ListView, DetailView

from .models import Post, PostCategory


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news_list.html'
    context_object_name = 'news'


class NewsInfo(DetailView):
    model = Post
    template_name = 'news_info.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['text'] = obj.text.split("\n")
        categories = PostCategory.objects.filter(post=obj)
        context['category_names'] = ", ".join([category.category.name for category in categories])
        return context
