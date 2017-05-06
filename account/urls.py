from django.conf.urls import url
from . import views
from django.contrib.auth.views import login,logout
from account.views import UserProfileEdit,Profileupload,Search_results,Profile,People_search,createblog,blog,Myblog,signup

urlpatterns=[url(r'^$', views.login),
             url(r'^login/$', login,{'template_name':'login/login.html'} ),
             url(r'^logout/$', logout,{'template_name':'logout/logout.html'}),
             url(r'^signup/$', signup.as_view(), name='signup'),
             url(r'^profile/$', Profile.as_view(), name='profile'),
             url(r'^settings/$', views.settings, name='settings'),
             url(r'^psettings/$',views.psettings,name='psettings'),
             url(r'^ensettings/$',views.ensettings,name='ensettings'),
             url(r'^changepassword/$',views.changepassword,name='changepassword'),
             url(r'^blogs/$', views.blogs, name='blogs'),
             url(r'^newspapers/$', views.newspapers, name='newspapers'),
             url(r'^Newspapers/$', views.newspapers, name='newspapers'),
             url(r'^Welcome-to-socrates/$', views.Welcome,name='Welcome'),
             url(r'^profile/basic_edit/$',views.UserBasicEdit,name='UserBasicEdit'),
             url(r'^profile/User_profile/$', UserProfileEdit.as_view(),name='UserProfileEdit'),
             url(r'^profile/upload_picture/$', Profileupload.as_view(),name='Upload'),
             url(r'^searchsocrates/$',Search_results.as_view(),name='searchprimary'),
             url(r'^search_people/$', People_search.as_view(),name='peoplesearch'),
             url(r'^createblog/$', createblog.as_view(),name='createblog'),
             url(r'^blog/$',blog.as_view(),name='blog'),
             url(r'^Myblog/$',Myblog.as_view(),name='Myblog'),
             url(r'^viewprofile/(?P<pk>.+)/$', views.viewprofile,name='viewprofile'),
             url(r'^connect/(?P<action>.+)/(?P<pk>\d+)/$',views.connections,name='connections'),
             url(r'^(?P<user>.+)/following/$',views.imfollowing,name='following'),
             url(r'^(?P<user>.+)/followers/$',views.myfollowers,name='followers'),

            ]
