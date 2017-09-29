from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class NetUserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    email = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
    def __str__(self):
        return self.uname

class Post(models.Model):
    # 作者
    author = models.ForeignKey(NetUserInfo)
    # 标题
    title = models.CharField(max_length=200)
    # 文章内容
    text = models.TextField()
    #　创建日期
    created_date = models.DateTimeField(default=timezone.now)
    # 发布日期
    published_date = models.DateTimeField(blank=True, null=True)
    # 关键字
    keywords = models.CharField(max_length=30,null=True,blank=True)

    #　点击量
    click = models.IntegerField(default=0)

    # 点赞数
    praise = models.IntegerField(default=0)

    # 踩
    cai = models.IntegerField(default=0)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class BlogClick(models.Model):
    #　用户
    user = models.ForeignKey(NetUserInfo)
    # 文章
    post = models.ForeignKey(Post)
    # 评论
    discuss = models.TextField()
    def __str__(self):
        return self.discuss
