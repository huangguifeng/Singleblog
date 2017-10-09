from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from haystack.generic_views import SearchView
from .decortion import is_click,is_login,is_not_login
from hashlib import sha1
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from .duanzi_spider import DuanZi
# Create your views here.


def index(request):
    index= int(request.GET.get('index','1'))
    blog = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    page = Paginator(blog,5)
    blog = page.page(index)
    context = {"blog":blog}
    return render(request,'blog/index.html',context)


def post_detail(request,id):
    c = Post.objects.get(id=int(id))

    c.click += 1
    c.save()
    context = {'content':c,'uname':'您'}
    return render(request,'blog/post_detail.html',context)

@is_login
def newblog(request):

    #　判断这个用户账号是否有写博客的权限
    uid = request.session['uid']
    user = NetUserInfo.objects.get(id=uid)
    if user.admin == 1:
        context = {'title':'写博客'}
        return render(request,'blog/newblog.html',context)
    else:
        return render(request,'blog/power_tip.html')

def application(request):
    # 写博客权限申请
    uid = request.session['uid']
    dict = request.POST
    email = dict.get('email','')
    text = dict.get('text','')
    context = {'email':email,"text":text}
    if email=="" or text== "":
        return render(request, 'blog/power_tip.html',context)
    else:
        #发送邮件给指定管理审核
        user = NetUserInfo.objects.filter(id=uid)
        username = user[0].uname
        upwd = user[0].upwd[:10]

        try:
            msg = '<p>用户：%s　申请写博客权限。</p><a href="http://itpython.pythonanywhere.com/authorize/?uid=%s&pwd=%s&email=%s" target="_blank">点击快速授权</a>'%(username,uid,upwd,email)
            msgs = msg+"\n\n" +'申请内容：'+text
            send_mail('%s申请博客授权'%username, '', settings.EMAIL_FROM,
                  ['pydjango@163.com'],
                  html_message=msgs)
        except Exception as e :
            print(e)
        return render(request,'blog/wait.html')

def authorize(request):
    uid = request.GET.get('uid')
    pwd = request.GET.get('pwd')
    email = request.GET.get('email')
    user = NetUserInfo.objects.get(id=uid)
    spwd = user.upwd[:10]
    if pwd == spwd:
        user.admin = 1
        try:
            msg = '博客管理权限申请成功，本邮件有系统发送，请勿回复！'

            send_mail('博客管理权限申请成功，本邮件有系统发送，请勿回复！', '', settings.EMAIL_FROM,
                      [email],
                      html_message=msg)
        except Exception as e:
            print(e)
        return  HttpResponse('ok')
    else:
        return HttpResponse('用户密码校验失败.')





# 保存写入的博客
def insert(request):
    dict = request.POST
    author = request.session['uid']
    title = dict.get('title','')
    keywords = dict.get('keywords','')
    text = dict.get('content','')
    content = {'title':'写博客','blogtitle':title,'keywords':keywords,'text':text}
    if title == "" or keywords =="" or content=='':
        return render(request,'blog/newblog.html',content)
    else:
        blog = Post()
        blog.author_id = author
        blog.title = title
        blog.keywords = keywords
        blog.text = text
        blog.save()
        return redirect('/manage/')


class BlogSearchView(SearchView):
    '''
    全文检索
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dz = DuanZi()
        result = dz.load_page()
        context['dz'] = result
        return context


# 赞
@is_click
def top(request):
    blog_id = request.GET.get('id')
    post = Post.objects.get(id=blog_id)
    post.praise += 1
    post.save()
    return JsonResponse({'num':post.praise,'is_error':1})


# 踩
@is_click
def step(request):
    blog_id = request.GET.get('id')
    post = Post.objects.get(id=blog_id)
    post.cai += 1
    post.save()
    return JsonResponse({'num': post.cai,'is_error':1})


# 保存评论处理
def discuss(request):
    '''
    还需要写入到数据库,需要接收，评论用户，文章ｉｄ，
    :param request:
    :return:
    '''
    if 'uid' not in request.session:
        return JsonResponse({"error":1})
    dict = request.POST

    uid = request.session['uid']
    text = dict.get('text')
    wid = dict.get("wid")
    bc = BlogClick()

    bc.user_id = int(uid)
    bc.post_id = int(wid)
    bc.discuss=text
    bc.save()
    return JsonResponse({'code':'ok'})


def pinlun(request):
    '''
    展示评论
    :param request:
    :return:
    '''
    wid = request.GET.get('wid')
    items = []
    pl = BlogClick.objects.filter(post_id=int(wid)).order_by("id")
    if pl:
        for i in pl:
            item = {}
            item['username'] = i.user.uname
            item['text'] = i.discuss
            items.append(item)
        return JsonResponse({"pl":items})
    else:
        return JsonResponse({'pl':'empty'})

@is_not_login
def login(request):

    #　处理登陆注册
    if request.method == 'GET':
        return render(request,'blog/login.html')

    elif request.method == 'POST':
        to = request.POST.get('to')
        if to == "reg":
            # 　注册
            dict = request.POST
            user = dict.get("user")
            passwd = dict.get("passwd")
            email = dict.get("email")
            userinfo = NetUserInfo()
            # 用户密码ｓｈａ1加密保存
            sha_pwd = sha1()
            sha_pwd.update(bytes(passwd.encode()))
            s_pwd = sha_pwd.hexdigest()

            userinfo.uname = user
            userinfo.upwd = s_pwd
            userinfo.email = email

            userinfo.save()
            return render(request,'blog/welcome1.html',context={'user':user})
        elif to == "log":
            #  登陆

            dict = request.POST
            user = dict.get("username")
            passwd = dict.get("p")

            user_list = NetUserInfo.objects.filter(uname=user)
            if user_list:
                #　如果用户名存在
                sha_pwd = sha1()
                sha_pwd.update(bytes(passwd.encode()))
                s_pwd = sha_pwd.hexdigest()
                print(s_pwd)
                if user_list[0].upwd == s_pwd:
                    #　密码正确
                    request.session['user'] = user
                    request.session['uid'] = user_list[0].id
                    response = redirect('/')
                    response.set_cookie('user',user)
                    return response
            #账号或密码不正确
            context = {'userName':user,'error': 1}
            return render(request,'blog/login.html',context)


def logout(request):
    '''
    退出登录
    '''
    request.session.flush()
    response = redirect('/login/')
    response.set_cookie('user',max_age=-1)
    return response

def verify(request):
    '''
    验证用户名是否存在
    :param request:
    :return:
    '''
    dict = request.POST
    user = dict.get('username')
    userinfo = NetUserInfo.objects.filter(uname=user)
    if userinfo:
        # 用户名存在
        return JsonResponse({'ucode':1})
    else:
        # 用户名不存在
        return JsonResponse({'ucode': 0})


def protocol(request):
    # 用户协议
    return render(request,'blog/user_protocol.html')


def pull(request):
    '''
    获取最新发布，新评论，热门文章，返回json给前端展示
    :param reqeust:
    :return:
    '''
    #最新文章
    wz_json={}
    wz = Post.objects.filter(published_date__isnull=False).order_by('-id')[0:4]
    for i in wz:
        wz_json[i.id]=i.title
     #最新评论
    dis = BlogClick.objects.all().order_by('-id')[0:4]
    dis_json={}
    for i in dis:
        ds={}
        ds['title']= i.post.title
        ds['id']=i.post.id
        dis_json[i.discuss] = ds
    #最热
    zr_json={}
    zr_list =  Post.objects.filter(published_date__isnull=False).order_by('-click')[0:4]
    for i in zr_list:
        zr_json[i.id]=i.title
    return JsonResponse({"wz":wz_json,"zr":zr_json,"dis":dis_json})


def resume(request):
    '''关于页面'''
    return render(request,'blog/resume.html')


def manage(request):

    '''博文页面'''
    if 'uid' in request.session:

        uid = request.session['uid']
        user  = NetUserInfo.objects.get(id=uid)
        if user.admin:
            p_list = Post.objects.all()
            code = 1
        else:
            p_list = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
            code = 0
    else:
        p_list = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
        code = 0
    context = {'post': p_list,'code':code}
    return render(request, 'blog/manage.html', context)


def modify(request):
    '''修改文章'''
    id = request.GET.get('id')
    p = Post.objects.get(id=id)
    context={"blogtitle":p.title,'keywords':p.keywords,'text':p.text}
    p.delete()
    return render(request,'blog/newblog.html',context)


def delete(request):
    '''删除文章'''
    id=request.GET.get('id')
    p=Post.objects.get(id=id)
    p.delete()
    return redirect('/manage/')

def pub(reqeust):
    '''
    发布文章
    '''
    id = reqeust.GET.get('id')
    p = Post.objects.get(id=id)
    p.publish()

    return redirect('/manage/')

