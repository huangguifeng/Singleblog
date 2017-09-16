from django.shortcuts import render
from .models import *
from django.http import HttpResponse
# Create your views here.
def index(request):
    bolg = Post.objects.all()
    context = {"blog":bolg}
    return render(request,'blog/index.html',context)
