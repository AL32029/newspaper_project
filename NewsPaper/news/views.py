import re

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from .filters import NewsFilter
from .forms import NewsForm
from .models import Post, PostCategory, UserCategory, Category, Author
from .tasks import send_new_post_category


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    post_type = None
    template_name = None
    context_object_name = None
    paginate_by = 10
    
    def setup(self, request: HttpRequest, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = re.findall(r'(news|articles)', request.path)[0] if kwargs.get("post_type") is None else kwargs.get("post_type")
        self.template_name = f'{self.post_type}/list.html'
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
        self.post_type = re.findall(r'(news|articles)', request.path)[0] if kwargs.get("post_type") is None else kwargs.get("post_type")
        self.template_name = f'{self.post_type}/search.html'
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
        self.post_type = re.findall(r'(news|articles)', request.path)[0] if kwargs.get("post_type") is None else kwargs.get("post_type")
        self.template_name = f'{self.post_type}/info.html'
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
        categories_subscribes = [
            user_category.category
            for user_category in UserCategory.objects.filter(
                user=self.request.user,
                category__in=[cat.category for cat in categories]
            )
        ]
        categories_text = []
        for category_item in categories:
            is_subscribed = category_item.category in categories_subscribes
            url = (f'<a href="/{"unsubscribe" if is_subscribed else "subscribe"}_category/{category_item.category.id}/?return_to={self.request.path}">'
                   f'{"Отписаться" if is_subscribed else "Подписаться"}</a>')
            categories_text.append(f"{category_item.category.name} ({url})")
        context['category_names'] = ", ".join(categories_text)

        context['is_author'] = self.object.author.user == self.request.user
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = (
        'news.add_post'
    )
    form_class = NewsForm
    model = Post
    post_type = None
    template_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = re.findall(r'(news|articles)', request.path)[0] if kwargs.get("post_type") is None else kwargs.get("post_type")
        self.template_name = f'{self.post_type}/create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = "NE" if self.post_type == "news" else "AR"
        news.author_id = Author.objects.filter(user_id=self.request.user).first().id
        news.save()
        if form.cleaned_data.get("category") is not None:
            PostCategory.objects.create(category=Category.objects.filter(id=form.cleaned_data.get("category")).first(), post=news)
        response = super().form_valid(form)
        send_new_post_category(self.object.id)
        return response

    def get_success_url(self):
        return f'/{self.post_type}/{self.object.id}'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = (
        'news.change_post'
    )
    form_class = NewsForm
    model = Post
    post_type = None
    template_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = re.findall(r'(news|articles)', request.path)[0] if kwargs.get("post_type") is None else kwargs.get("post_type")
        self.template_name = f'{self.post_type}/update.html'

    def get_object(self, queryset=None):
        object = super().get_object()
        if object.author.user != self.request.user:
            raise PermissionDenied("Данный пост не принадлежит вам")
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_id'] = self.object.id
        context['is_author'] = self.object.author.user == self.request.user
        return context


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    post_type = None
    template_name = None
    success_url = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_type = re.findall(r'(news|articles)', request.path)[0] if kwargs.get("post_type") is None else kwargs.get("post_type")
        self.template_name = f'{self.post_type}/delete.html'
        self.success_url = reverse_lazy(f'{self.post_type}_list')

    def get_object(self, queryset=None):
        object = super().get_object()
        if object.author.user != self.request.user:
            raise PermissionDenied("Данный пост не принадлежит вам")
        return object

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['news_id'] = obj.id
        context['is_author'] = self.object.author.user == self.request.user
        return context
