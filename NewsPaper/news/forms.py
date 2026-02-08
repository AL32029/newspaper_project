from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


class NewsForm(forms.ModelForm):
    """
    Форма для постов
    """
    category = forms.ChoiceField(
        choices=((category.id, category.name) for category in Category.objects.all())
    )
    class Meta:
        model = Post
        fields = ['title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 15:
            raise ValidationError({
                "title": "Длина заголовка новости меньше 15 символов"
            })
        text = cleaned_data.get("text")
        if text is not None and len(text) < 30:
            raise ValidationError({
                "text": "Длина текста новости меньше 30 символов"
            })
        return cleaned_data
