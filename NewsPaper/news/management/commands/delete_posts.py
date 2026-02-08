from django.core.management.base import BaseCommand, CommandError
from news.models import Category, PostCategory, Post


class Command(BaseCommand):
    help = "Команда предназначена для удаления всех постов определенной категории"

    missing_args_message = "Недостаточно аргументов для запуска команды"

    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category_id', type=int)

    def handle(self, *args, **options):
        self.stdout.readable()
        category = Category.objects.filter(pk=int(options['category_id'])).first()
        if category is None:
            raise CommandError(f'Категория с ID {options['category_id']} не обнаружена')
        posts = PostCategory.objects.filter(category=category).values_list('post', flat=True)
        if len(posts) == 0:
            raise CommandError(f"В категории «{category.name}» отсутствуют посты")
        self.stdout.write(
            f"В категории «{category.name}» обнаружено {len(posts)} постов. Желаете удалить все посты? yes/no"
        )
        answer = input()
        if answer == "yes":
            Post.objects.filter(pk__in=posts).delete()
            self.stdout.write(f"Успешно удалено {len(posts)} постов!")
            return
        self.stdout.write("Действие отменено")
