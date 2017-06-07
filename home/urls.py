from django.conf.urls import url
from . import views
from .views import unitednations,home,homeSports,homeMarket

urlpatterns=[url(r'^(?P<filter>[\w]+)$', home.as_view(), name='home'),


             url(r'^visitors/(?P<pk>[0-9]+)/$', views.visits,name='visits'),
             url(r'^suggestion/(?P<pk>[0-9]+)/$', views.suggest,name='suggest'),
             url(r'^make_comment/(?P<pk>[0-9]+)/$',views.post_comment,name='post_comment'),
             url(r'^remove_comment/(?P<pk>[0-9]+)/$',views.remove_comment,name='remove_comment'),
             url('^vote/(?P<action>[\w.@+-]+)/(?P<pk>[0-9]+)/$', views.sociallike,name='sociallike'),
             url(r'^Politics/(?P<filter>.+)$',home.as_view(),name='home'),
             url(r'^politics/(?P<filter>.+)$',home.as_view(),name='home'),
             url(r'^Sports/$',homeSports.as_view(),name='home-sports'),
             url(r'^sports/$',homeSports.as_view(),name='home-sports'),
             url(r'^Market/$',homeMarket.as_view(),name='home-market'),
             url(r'^market/$',homeMarket.as_view(),name='home-market'),
             url(r'^UnitedNations/(?P<filter>.+)$',unitednations.as_view(),name='home-unitednations'),
             ]
