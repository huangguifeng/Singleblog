from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Post(models.Model):
    # 作者
    author = models.ForeignKey(User)
    # 标题
    title = models.CharField(max_length=200)

    # 文章内容
    text = HTMLField()
    #　创建日期
    created_date = models.DateTimeField(default=timezone.now)
    # 发布日期
    published_date = models.DateTimeField(blank=True, null=True)

    # 关键字
    keywords = models.CharField(max_length=20,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title