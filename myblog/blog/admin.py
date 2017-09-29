from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(NetUserInfo)
admin.site.register(BlogClick)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title']
    class Media:
        # 在管理后台的HTML文件中加入js文件, 每一个路径都会追加STATIC_URL/
        js = (
            '/static/js/editor/kindeditor/kindeditor-all-min.js',
            '/static/js/editor/kindeditor/zh_CN.js',
            '/static/js/editor/kindeditor/config.js',
        )


