from django.conf.urls import url
# from django.urls import re_path
from . import views

urlpatterns = [url(r'^$', views.index, name='home'),
               url(r'^upload$', views.upload, name='upload'),
               url(r'^login$', views.admin, name='upload'),
               url(r'^home$', views.home, name='upload'),
               url(r'^logout$', views.logout, name='upload'),
               url(r'^register$', views.register, name='upload'),
            url(r'^add$', views.add, name='upload'),
               url(r'^recipe/(?P<username>[\w. @+-]+)/$', views.detail, name='user'),
url(r'^recipe/(?P<username>[\w. @+-]+)/rate$', views.ratings, name='user'),
               url(r'^edit/(?P<username>[\w. @+-]+)/$', views.edit, name='user'),
               url(r'^byingredient$', views.byingredient, name='byingrdients')]
