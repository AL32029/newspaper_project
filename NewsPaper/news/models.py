from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models


class Author(models.Model):
    """
    Модель автора
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """
        Актуализация рейтинга автора (на основе рейтинга постов, комментариев)
        """
        posts_rating = Post.objects.filter(author=self).aggregate(
            total=models.Sum('rating')
        )['total'] or 0
        comments_rating = Comment.objects.filter(user=self.user).aggregate(
            total=models.Sum('rating')
        )['total'] or 0
        comments_posts_rating = Comment.objects.filter(post__author=self).aggregate(
            total=models.Sum('rating')
        )['total'] or 0

        self.rating = sum([posts_rating * 3, comments_rating, comments_posts_rating])
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """
    Модель категории
    """
    name = models.CharField(max_length=255, unique=True)
    subscribes = models.ManyToManyField(User, through="UserCategory")


class Post(models.Model):
    """
    Модель поста
    """
    news = 'NE'
    article = 'AR'

    POST_TYPES = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through="PostCategory")

    def like(self):
        """
        Лайк к посту
        """
        self.rating += 1
        self.save()

    def dislike(self):
        """
        Дизлайк к посту
        """
        self.rating -= 1
        self.save()

    def preview(self):
        """
        Получение урезанного заголовка поста
        """
        return self.text[:124] + ("..." if len(self.text) > 124 else "")

    def get_absolute_url(self):
        """
        Получение абсолютной ссылки на пост (с доменом)
        """
        domain = Site.objects.get_current().domain
        return f'http://{domain}/{'news' if self.post_type == 'NE' else 'articles'}/{self.pk}'

    def save(self, *args, **kwargs):
        """
        Сохранение изменений в посте (с удалением из кеша)
        """
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    """
        Модель для Many-To-Many связи между Post и Category
        """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    """
    Модель комментариев к постам
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        """
        Лайк к посту
        """
        self.rating += 1
        self.save()

    def dislike(self):
        """
        Дизлайк к посту
        """
        self.rating -= 1
        self.save()


class UserCategory(models.Model):
    """
    Модель для Many-To-Many связи между User и Category
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
