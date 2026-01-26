from typing import Any

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import NewsFilter
from .forms import NewsForm, ArticlesForm
from .models import Post, PostCategory


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    post_type = None
    template_name = None
    context_object_name = None
    paginate_by = 10
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = kwargs.get("post_type")
        self.template_name = f'{self.post_type}_list.html'
        self.context_object_name = self.post_type.__str__()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='NE' if self.post_type == "news" else "AR"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_type'] = self.post_type
        return context


class NewsSearch(ListView):
    model = Post
    ordering = '-created_at'
    post_type = None
    template_name = None
    context_object_name = None
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = kwargs.get("post_type")
        self.template_name = f'{self.post_type}_search.html'
        self.context_object_name = self.post_type.__str__()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='NE' if self.post_type == "news" else "AR"
        )
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class NewsInfo(DetailView):
    model = Post
    post_type = None
    template_name = None
    context_object_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = kwargs.get("post_type")
        self.template_name = f'{self.post_type}_info.html'
        self.context_object_name = self.post_type.__str__()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='NE' if self.post_type == "news" else "AR"
        )
        return queryset

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['text'] = obj.text.split("\n")
        categories = PostCategory.objects.filter(post=obj)
        context['category_names'] = ", ".join([category.category.name for category in categories])
        return context


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    post_type = None
    template_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = kwargs.get("post_type")
        self.template_name = f'{self.post_type}_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = "NE" if self.post_type == "news" else "AR"
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    post_type = None
    template_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = kwargs.get("post_type")
        self.template_name = f'{self.post_type}_update.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['news_id'] = obj.id
        return context


class NewsDelete(DeleteView):
    model = Post
    post_type = None
    template_name = None
    success_url = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = kwargs.get("post_type")
        self.template_name = f'{self.post_type}_delete.html'
        self.success_url = reverse_lazy(f'{self.post_type}_list')

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['news_id'] = obj.id
        return context
