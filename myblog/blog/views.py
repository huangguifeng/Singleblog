from django.shortcuts import render
from .models import *
from django.http import HttpResponse
# Create your views here.
def index(request):
    list = Post.objects.all()
    context = {"list":list}
    return HttpResponse('ok')
