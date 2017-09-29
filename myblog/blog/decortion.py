from django.http import JsonResponse
from django.shortcuts import redirect
import time
# 　装饰器


def is_click(func):
    '''
    判断用户点击赞或踩的时间超过一天
    '''
    def inner(request):
        blog_id = request.GET.get("id")
        now_time = int(time.time())
        if blog_id in request.session:
            is_time = request.session[blog_id]
            if int(is_time) > now_time:
                return JsonResponse({'is_error':0})
        request.session[blog_id] = now_time+60*60*24
        return func(request)
    return inner


def is_login(func):
    '''
    #判断是否登陆如果登陆执行函数，没有登陆重定向到登陆界面
    '''
    def inner(request):
        if 'uid' in request.session:
            return func(request)
        else:
            return redirect('/login/')
    return inner

def is_not_login(func):
    '''
    #判断是否登陆如果登陆执行函数，没有登陆重定向到登陆界面
    '''
    def inner(request):
        if 'uid' in request.session:
            return redirect('/')
        else:
            return func(request)
    return inner