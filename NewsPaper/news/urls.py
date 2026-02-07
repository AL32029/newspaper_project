"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.views.decorators.cache import cache_page

from .views import NewsList, NewsInfo, NewsSearch, NewsCreate, NewsDelete, NewsUpdate

urlpatterns = [
    path('', cache_page(60*5)(NewsList.as_view()), name="articles_list"),
    path('create/', NewsCreate.as_view(), name="articles_create"),
    path('search/', NewsSearch.as_view(), name="articles_search"),
    path('<int:pk>', NewsInfo.as_view(), name="articles_info"),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='articles_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='articles_delete')
]
