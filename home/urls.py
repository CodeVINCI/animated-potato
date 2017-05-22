from django.conf.urls import url
from . import views
from .views import unitednations,home

urlpatterns=[url(r'^(?P<filter>[\w]+)$', home.as_view(), name='home'),
             url(r'^visitors/(?P<pk>[0-9]+)/$', views.visits,name='visits'),
             url(r'^suggestion/(?P<pk>[0-9]+)/$', views.suggest,name='suggest'),
             url('^vote/(?P<action>[\w.@+-]+)/(?P<pk>[0-9]+)/$', views.sociallike,name='sociallike'),
             url(r'^Politics/(?P<filter>.+)$',home.as_view(),name='home'),
             url(r'^politics/(?P<filter>.+)$',home.as_view(),name='home'),
             url(r'^Sports/$',views.homeSports,name='home-sports'),
             url(r'^sports/$',views.homeSports,name='home-sports'),
             url(r'^Market/$',views.homeMarket,name='home-market'),
             url(r'^market/$',views.homeMarket,name='home-market'),
             url(r'^UnitedNations/$',unitednations.as_view(),name='home-unitednations'),
             url(r'^unitednations/$',unitednations.as_view(),name='home-unitednations'),
             ]
