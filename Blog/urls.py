from django.conf.urls import url,include
from Blog import views

app_name = 'Blog'
urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<id>[0-9]+)/$', views.category, name='category'),
    url(r'^tag/(?P<id>[0-9]+)/$', views.tags, name='tag'),

]

