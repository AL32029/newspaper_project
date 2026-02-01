from django.http.request import HttpRequest
from django.shortcuts import render

from news.models import Post


def index_view(request: HttpRequest):
    return render(request, 'main_templates/index.html', {
        "posts": Post.objects.order_by("-created_at")[:10]
    })