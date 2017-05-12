from django.conf.urls import url
from . import views
from .views import unitednations,home

urlpatterns=[url(r'^$', home.as_view(), name='home'),
             url(r'^Politics/$',views.home,name='home'),
             url(r'^politics/$',views.home,name='home'),
             url(r'^Sports/$',views.homeSports,name='home-sports'),
             url(r'^sports/$',views.homeSports,name='home-sports'),
             url(r'^Market/$',views.homeMarket,name='home-market'),
             url(r'^market/$',views.homeMarket,name='home-market'),
             url(r'^UnitedNations/$',unitednations.as_view(),name='home-unitednations'),
             url(r'^unitednations/$',unitednations.as_view(),name='home-unitednations'),
             ]
