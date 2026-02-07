from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from .models import PostCategory
from .tasks import send_message_new_post, send_message_new_user


@receiver(post_save, sender=PostCategory)
def notify_new_post(sender, instance: PostCategory, created, **kwargs):
    post = instance.post
    category = instance.category
    send_message_new_post.apply_async((post.id, category.id,))


@receiver(post_save, sender=User)
def new_user(sender, instance: User, created, **kwargs):
    if instance.email is not None:
        send_message_new_user.apply_async((instance.pk,))
