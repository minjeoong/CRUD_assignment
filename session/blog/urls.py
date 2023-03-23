from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
]

# 127.0.0.1:8000/blog/hello