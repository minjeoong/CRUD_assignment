from django.shortcuts import render
# Create your views here.
from .models import Blog
from django.http import HttpResponse

def blog(request):
    blog = Blog.objects.all()
    return HttpResponse(blog)
    