from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author']

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

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 15:
            raise ValidationError({
                "title": "Длина заголовка статьи меньше 15 символов"
            })
        text = cleaned_data.get("text")
        if text is not None and len(text) < 30:
            raise ValidationError({
                "text": "Длина текста статьи меньше 30 символов"
            })
        return cleaned_data