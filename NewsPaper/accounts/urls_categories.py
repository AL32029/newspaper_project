from django.urls.conf import path

from .views import subscribe_category

urlpatterns = [
    path('<int:category_id>/', subscribe_category)
]