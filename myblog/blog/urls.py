from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^blog/(\d+)/$',views.post_detail),
    url(r'^blog/new/',views.newblog),
    # url('^search/$', views.BlogSearchView.as_view())

]




