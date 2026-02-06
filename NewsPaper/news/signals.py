from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.loader import render_to_string

from .models import PostCategory, UserCategory

# TODO: Добавить гиперссылку на пост
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