from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from news.models import Post

@cache_page(60)
def index_view(request: HttpRequest):
    return render(request, 'main_templates/index.html', {
        "posts": Post.objects.order_by("-created_at")[:10]
    })