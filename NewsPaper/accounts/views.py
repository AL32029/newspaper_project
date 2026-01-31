from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from news.models import Post, Author


@login_required
def profile_view(request):
    is_author = request.user.groups.filter(name="author").exists()
    posts = None
    if is_author:
        posts = Post.objects.filter(author__user=request.user).order_by("-created_at")
    return render(request, 'account/profile.html', {
        "is_author": is_author,
        "posts": posts
    })


@login_required
def get_status_author(request):
    user = request.user
    author_group = Group.objects.get(name="author")
    if not user.groups.filter(name="author").exists():
        author_group.user_set.add(user)
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(
           user=user
        )
    return redirect("/accounts/profile/")
