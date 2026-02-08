from django.contrib import admin
from .models import Category, Post


class PostsAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Post._meta.get_fields()
        if field.__class__.__name__ not in [
            'ManyToManyField',
            'ForeignKey',
            'OneToOneField',
            'ManyToOneRel',
            'ManyToManyRel'
        ]
           and not field.is_relation
    ]

    list_filter = ('post_type', 'created_at',)
    search_fields = ('title',)

class CategoriesAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Category._meta.get_fields()
        if field.__class__.__name__ not in [
            'ManyToManyField',
            'ForeignKey',
            'OneToOneField',
            'ManyToOneRel',
            'ManyToManyRel'
        ]
           and not field.is_relation
    ]

    list_filter = ('name', )


admin.site.register(Category, CategoriesAdmin)
admin.site.register(Post, PostsAdmin)
