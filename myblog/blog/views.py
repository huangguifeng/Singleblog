from django.shortcuts import render
from .models import *
from django.http import HttpResponse
# Create your views here.


def index(request):
    bolg = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    context = {"blog":bolg}
    return render(request,'blog/index.html',context)


def post_detail(request,id):
    content = Post.objects.get(id=int(id))
    context = {'content':content}
    return render(request,'blog/post_detail.html',context)


def newblog(request):
    pass