from django.urls.conf import path, include

urlpatterns = [
    path('', include('allauth.urls'))
]