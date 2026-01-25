from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import NewsFilter
from .forms import NewsForm, ArticlesForm
from .models import Post, PostCategory


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='NE'
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class NewsSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='NE'
        )
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class NewsInfo(DetailView):
    model = Post
    template_name = 'news_info.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='NE'
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
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = "NE"
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_update.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['news_id'] = obj.id
        return context


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['news_id'] = obj.id
        return context


class ArticlesList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'articles_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='AR'
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ArticlesSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'articles_search.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='AR'
        )
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class ArticlesInfo(DetailView):
    model = Post
    template_name = 'articles_info.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            post_type='AR'
        )
        return queryset

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['text'] = obj.text.split("\n")
        categories = PostCategory.objects.filter(post=obj)
        context['category_names'] = ", ".join([category.category.name for category in categories])
        return context


class ArticlesCreate(CreateView):
    form_class = ArticlesForm
    model = Post
    template_name = 'articles_create.html'

    def form_valid(self, form):
        articles = form.save(commit=False)
        articles.post_type = "AR"
        return super().form_valid(form)


class ArticlesUpdate(UpdateView):
    form_class = ArticlesForm
    model = Post
    template_name = 'articles_update.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['articles_id'] = obj.id
        return context


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('articles_list')

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['articles_id'] = obj.id
        return context
