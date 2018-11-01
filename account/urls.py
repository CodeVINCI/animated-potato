from django.conf.urls import url
from . import views
from account.views import UserProfileEdit,Profileupload,Search_results,Profile,People_search,signup,newspapers,ComparePublish,ComparePublished
from django.contrib.auth.views import login,logout,password_reset,password_reset_done,password_reset_confirm,password_reset_complete
from . import ajax

urlpatterns=[url(r'^$', views.login),
             url(r'^login/$', login,{'template_name':'login/login.html'} ),
             url(r'^logout/$', logout,{'template_name':'logout/logout.html'}),
             url(r'^deactivate/$', views.deactivate, name='deactivate'),
             
             url(r'^dictionary/$', ajax.dictionary, name='dictionary'),

             url(r'^signup/$', signup.as_view(), name='signup'),
             url(r'^profile/$', Profile.as_view(), name='profile'),
             url(r'^markallread/$', views.allread, name='allread'),

             url(r'^compare/$', ComparePublish.as_view(), name='compare'),
             url(r'^publishedcompare/$', ComparePublished.as_view(), name='publishedcompare'),

             url(r'^newcompare/$',ajax.newcompare, name='newcompare'),
             url(r'^addposttocompare/$',ajax.addposttocompare, name='addposttocompare'),

             url(r'^settings/$', views.settings, name='settings'),
             url(r'^psettings/$',views.psettings,name='psettings'),
             url(r'^ensettings/$',views.ensettings,name='ensettings'),
             url(r'^changepassword/$',views.changepassword,name='changepassword'),

             #url(r'^blogs/$', views.blogs, name='blogs'),
             url(r'^save/readlater/(?P<pk>[0-9]+)$', views.savepost, name='savepost'),
             url(r'^remove/readlater/(?P<pk>[0-9]+)$', views.removepost, name='removepost'),

             url(r'^newspapers/(?P<sitename>[\w.@+-]+)$', newspapers.as_view(), name='newspapers'),
             url(r'^Newspapers/(?P<action>[\w.@+-]+)$', newspapers.as_view(), name='newspapers'),

             url(r'^subscription/(?P<newssite>[\w.@+-]+)/(?P<action>[\w.@+-]+)/$',views.subscriptions,name='addrmsubscriptions'),
             url(r'^Welcome-to-socrates/$', views.Welcome,name='Welcome'),
             url(r'^profile/basic_edit/$',views.UserBasicEdit,name='UserBasicEdit'),
             url(r'^profile/User_profile/$', UserProfileEdit.as_view(),name='UserProfileEdit'),
             url(r'^profile/upload_picture/$', Profileupload.as_view(),name='Upload'),
             url(r'^searchsocrates/(?P<search_terms>.+)$',Search_results.as_view(),name='searchprimary'),
             url(r'^search_people/(?P<search_terms>.+)$', People_search.as_view(),name='peoplesearch'),

             url(r'^viewprofile/(?P<pk>[0-9]+)/$', views.viewprofile,name='viewprofile'),
             url(r'^viauserpk/(?P<pk>[0-9]+)/$', views.viauserpk,name='viauser'),
             url(r'^connect/(?P<action>.+)/(?P<pk>\d+)/$',views.connections,name='connections'),
             url(r'^(?P<user>[\w.@+-]+)/following/$',views.imfollowing,name='following'),
             url(r'^(?P<user>[\w.@+-]+)/subscriptions/$',views.mysubscription,name='subscriptions'),
             url(r'^(?P<user>[\w.@+-]+)/articles/$',views.myarticles,name='articles'),
             url(r'^(?P<user>[\w.@+-]+)/followers/$',views.myfollowers,name='followers'),
             url(r'^reset_password/$', password_reset,{'template_name':
             'edit/reset_password.html', 'email_template_name':'edit/reset_password_email.html'},name='reset_password'),

            url(r'^reset_password/done/$',password_reset_done,{'template_name':'edit/reset_password_done.html'},name='password_reset_done'),
            url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$',password_reset_confirm,
                 {'template_name':'edit/reset_password_confirm.html'}, name='password_reset_confirm'),
            url(r'^reset_password/complete/$',password_reset_complete,{'template_name':'edit/reset_password_complete.html'},name='password_reset_complete'),

            ]
