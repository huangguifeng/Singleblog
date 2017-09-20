from django.shortcuts import render
from .models import *
from haystack.generic_views import SearchView

from django.http import HttpResponse
# Create your views here.


def index(request):
    bolg = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    context = {"blog":bolg}
    return render(request,'blog/index.html',context)


def post_detail(request,id):
    con = Post.objects.get(id=int(id))
    con.click += 1
    con.save()
    context = {'content':con,'title':con.title}
    return render(request,'blog/post_detail.html',context)


def newblog(request):

    context = {'title':'写博客'}
    return render(request,'blog/newblog.html',context)


# class BlogSearchView(SearchView):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['username'] = 'xiaoming'
#         return  context