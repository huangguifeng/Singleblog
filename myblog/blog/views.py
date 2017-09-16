from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    list = Post.objects.all()
    context = {'list':list,}
    return render(request,'blog/index.html',context)
