from django.conf.urls import url

from comments import views

app_name = 'comments'
urlpatterns = [
    url(r'^comment/blog/(?P<post_id>[0-9]+)/$', views.blog_comment, name='blog_comment'),
]