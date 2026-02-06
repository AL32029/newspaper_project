from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail.message import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.loader import render_to_string

from .models import PostCategory, UserCategory, Post


@receiver(post_save, sender=PostCategory)
def notify_new_post(sender, instance: PostCategory, created, **kwargs):
    post = instance.post
    category = instance.category
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


@receiver(post_save, sender=User)
def new_user(sender, instance: PostCategory, created, **kwargs):
    if instance.email is not None:
        posts = Post.objects.order_by("-created_at")[:10]
        html_content = render_to_string(
            'new_user.html',
            {
                'user': instance,
                'last_posts': posts
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Поздравляем с успешной регистрацией!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            bcc=[instance.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
