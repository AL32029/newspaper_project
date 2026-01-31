from django.http.request import HttpRequest
from django.shortcuts import render

def index_view(request: HttpRequest):
    return render(request, 'main_templates/index.html')