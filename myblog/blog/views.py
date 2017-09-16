from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    list = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    context = {'list':list}
    return render(request,'blog/index.html',context)
