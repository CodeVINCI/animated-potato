from django.conf.urls import url
from . import views,ajax
from .views import unitednations,home,homeSports,homeMarket,hindi

urlpatterns=[url(r'^(?P<filter>[\w]+)$', home.as_view(), name='home'),
             url(r'^scroll/loadcontent/(?P<theme>[\w]+)$', views.loadcontent, name='loadcontent'),
             url(r'^visitors/(?P<pk>[0-9]+)/$', views.visits,name='visits'),
             url(r'^editcompare/(?P<pk>[0-9]+)/$', ajax.editcompare,name='editcompare'),
             url(r'^updatecompare/(?P<pk>[0-9]+)/$', ajax.updatecompare,name='updatecompare'),
             url(r'^suggestion/(?P<pk>[0-9]+)/$', views.suggest,name='suggest'),
             url(r'^seennotification/(?P<pk>[0-9]+)/$', ajax.seennotification,name='seennotification'),
             url(r'^suggestion_compare/(?P<pk>[0-9]+)/$', views.suggest_compare,name='suggest'),
             url(r'^make_comment/(?P<pk>[0-9]+)/$',views.post_comment,name='post_comment'),
             url(r'^make_compare_comment/(?P<pk>[0-9]+)/$',views.post_compare_comment,name='post_comment'),
             url(r'^remove_comment/(?P<pk>[0-9]+)/$',views.remove_comment,name='remove_comment'),
             url(r'^remove_compare_comment/(?P<pk>[0-9]+)/$',views.remove_compare_comment,name='remove_comment'),
             url('^vote/(?P<action>[\w.@+-]+)/(?P<pk>[0-9]+)/$', views.sociallike,name='sociallike'),
             url(r'^notification/(?P<type>[\w.@+-]+)/(?P<pk>[0-9]+)$',views.notificationpost,name='notification-post'),
             url(r'^Politics/(?P<filter>.+)$',home.as_view(),name='home'),
             url(r'^politics/(?P<filter>.+)$',home.as_view(),name='home'),
             url(r'^hindinews/(?P<filter>.+)$',hindi.as_view(),name='hindi'),
             url(r'^Sports/(?P<filter>.+)$',homeSports.as_view(),name='home-sports'),
             url(r'^sports/(?P<filter>.+)$',homeSports.as_view(),name='home-sports'),
             url(r'^Market/(?P<filter>.+)$',homeMarket.as_view(),name='home-market'),
             url(r'^market/(?P<filter>.+)$',homeMarket.as_view(),name='home-market'),
             url(r'^UnitedNations/(?P<filter>.+)$',unitednations.as_view(),name='home-unitednations'),

             ]
