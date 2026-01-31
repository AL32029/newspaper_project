from django.urls.conf import path, include

from .views import profile_view, get_status_author

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', profile_view),
    path('profile/get_author_status/', get_status_author)
]