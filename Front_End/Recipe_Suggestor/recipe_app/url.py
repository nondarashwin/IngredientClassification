from django.urls import re_path
# from django.urls import re_path
from . import views

urlpatterns = [re_path(r'^$', views.index, name='home'),
               re_path(r'^upload$', views.upload, name='upload'),
               re_path(r'^login$', views.admin, name='upload'),
               re_path(r'^home$', views.home, name='upload'),
               re_path(r'^logout$', views.logout, name='upload'),
               re_path(r'^register$', views.register, name='upload'),
            re_path(r'^add$', views.add, name='upload'),
               re_path(r'^recipe/(?P<username>[\w. @+-]+)/$', views.detail, name='user'),
re_path(r'^recipe/(?P<username>[\w. @+-]+)/rate$', views.ratings, name='user'),
               re_path(r'^edit/(?P<username>[\w. @+-]+)/$', views.edit, name='user'),
               re_path(r'^byingredient$', views.byingredient, name='byingrdients')]
