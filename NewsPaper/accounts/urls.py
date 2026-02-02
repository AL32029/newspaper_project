from django.urls.conf import path, include

from .views import profile_view, get_status_author, EditProfile

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', profile_view, name='user_profile'),
    path('profile/settings/', EditProfile.as_view()),
    path('profile/get_author_status/', get_status_author)
]