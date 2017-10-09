from django.conf.urls import include, url
from . import views
from blog.uploads import upload_image
urlpatterns = [
    url(r'^$',views.index),
    url(r'^blog/(\d+)/$',views.post_detail),
    url(r'^blog/new/',views.newblog),
    url(r'^search/$', views.BlogSearchView.as_view()),
    url(r'^top/$',views.top),
    url(r'^step/$', views.step),
    url(r'^insert/$',views.insert),
    url(r'^upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r"^discuss/$",views.discuss),
    url(r"^login/$",views.login),
    url(r'^login/verify/$',views.verify),
    url(r'^logout/$',views.logout),
    url(r'^protocol/$',views.protocol),
    url(r'^application/$',views.application),
    url(r'^pinlun/$',views.pinlun),
    url(r"^pull/$",views.pull),
    url(r'^resume/$',views.resume),
    url(r'^manage/$',views.manage),
    url(r'^modify/$',views.modify),
    url(r'^delete/$',views.delete),
    url(r'^pub/$',views.pub),
    url(r"^authorize/",views.authorize)
]




