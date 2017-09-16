from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    list = Post.objects.filter(published_date__isnull=True).order_by('-published_date')
    return render(request,'blog/index.html',list)
