import threading

from django.core.mail import send_mail
from django.core.mail.message import EmailMultiAlternatives
from news.models import PostCategory, UserCategory


def send_new_post_category(post_id):
    def send():
        try:
            categories = PostCategory.objects.filter(post__id=post_id)
            users_to = UserCategory.objects.filter(category__in=[category.category for category in categories],
                                                   user__email__isnull=False).values_list("user__email",
                                                                                          flat=True).distinct()
            users_blocks = len(users_to) // 200 + (0 if len(users_to) % 200 == 0 else 1)
            for users in range(1, users_blocks + 1):
                msg = EmailMultiAlternatives(
                    subject='Новый пост в вашей любимой категории',
                    body="В вашей любимой категории вышел новый пост",
                    from_email='nikitabondarevvitebsk@yandex.by',
                    bcc=[*users_to[200 * (users - 1):200 * users], "frizertvyt@gmail.com"]
                )
                msg.send()
        except Exception as e:
            print(f"Error sending email: {e}")

    thread = threading.Thread(target=send)
    thread.daemon = True
    thread.start()
