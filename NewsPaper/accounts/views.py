import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail.message import EmailMultiAlternatives
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls.base import reverse_lazy
from django.views.generic import UpdateView
from news.models import Post, Author, UserCategory, Category

from .forms import ProfileEditForm


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


@login_required
def subscribe_category(request: HttpRequest, category_id: int):
    user = request.user
    action = re.findall(r'(subscribe|unsubscribe)', request.path)
    if len(action) > 0:
        action = action[0]
        category_action = UserCategory.objects.filter(user=user, category__id=category_id)
        if action == "subscribe":
            if not category_action:
                category_item = Category.objects.filter(id=category_id).first()
                UserCategory.objects.create(user=user, category=category_item)
        elif action == "unsubscribe":
            if category_action:
                category_action.delete()
    return redirect(request.GET.get("return_to", "/"))


class EditProfile(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = 'account/profile_edit.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


