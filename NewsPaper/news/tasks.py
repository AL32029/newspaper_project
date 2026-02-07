import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils import timezone
from news.models import UserCategory, Post, Category, PostCategory


@shared_task
def send_message_new_post(post_id, category_id):
    post = Post.objects.filter(id=post_id).first()
    category = Category.objects.filter(id=category_id).first()
    users_to = UserCategory.objects.filter(
        category=category, user__email__isnull=False
    ).values_list("user__email", flat=True).distinct()
    users_blocks = len(users_to) // 200 + (0 if len(users_to) % 200 == 0 else 1)
    html_content = render_to_string(
        'new_post.html',
        {
            'post': post,
            'category': category
        }
    )
    for users in range(1, users_blocks + 1):
        msg = EmailMultiAlternatives(
            subject=f'Новый пост в вашей любимой категории «{category.name}»',
            from_email=settings.DEFAULT_FROM_EMAIL,
            bcc=[*users_to[200 * (users - 1):200 * users]]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_message_new_user(user_id):
    user = User.objects.filter(pk=user_id).first()
    posts = Post.objects.order_by("-created_at")[:10]
    html_content = render_to_string(
        'new_user.html',
        {
            'user': user,
            'last_posts': posts
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Поздравляем с успешной регистрацией!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=[user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_newsletter():
    date_now = timezone.now()
    date_start = date_now - timezone.timedelta(weeks=1)
    date_end = date_now - timezone.timedelta(days=1)
    categories = Category.objects.all()
    for category in categories:
        posts = PostCategory.objects.filter(category=category, post__created_at__range=(date_start, date_end))
        if len(posts) > 0:
            posts = [post.post for post in posts]
            subscribes = UserCategory.objects.filter(category=category).exclude()
            subscribes_to = [subscribe.user.email for subscribe in subscribes if subscribe.user.email is not None]
            subscribes_blocks = len(subscribes_to) // 200 + (0 if len(subscribes_to) % 200 == 0 else 1)
            html_content = render_to_string(
                'weekly_mailing.html',
                {
                    'posts': posts,
                    'category': category
                }
            )
            for users in range(1, subscribes_blocks + 1):
                msg = EmailMultiAlternatives(
                    subject=f'Сводка новостей категории «{category.name}» за прошедшую неделю',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    bcc=[*subscribes_to[200 * (users - 1):200 * users]]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
