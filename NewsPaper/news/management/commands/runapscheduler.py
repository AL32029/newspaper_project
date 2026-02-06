import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Category, UserCategory, PostCategory

logger = logging.getLogger(__name__)


def weekly_mailing():
    date_now = timezone.now()
    date_start = date_now - timezone.timedelta(weeks=1)
    date_end = date_now - timezone.timedelta(days=1)
    categories = Category.objects.all()
    for category in categories:
        posts = PostCategory.objects.filter(category=category, post__created_at__range=(date_start, date_end))
        if len(posts) == 0:
            continue
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


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_mailing,
            trigger=CronTrigger(
                day_of_week="mon", hour="12", minute="00"
            ),
            id="weekly_mailing",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_mailing'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")