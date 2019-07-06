"""forumProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from qaboard import views
from django.conf.urls import url
from userAccounts import views as accountsViews
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="forum-home_view"),
    path('signup/', accountsViews.signup_view, name='accounts-signup_view'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='accounts-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='accounts-logout'),
    url(r'^topics/(?P<pk>\d+)/$', views.topic_ques, name='forum-topic_ques'),
    url(r'^topics/(?P<pk>\d+)/new/$', views.new_ques, name='forum-new_ques'),
    url(r'^topics/(?P<pk>\d+)/questions/(?P<ques_pk>\d+)/$', views.ques_ans, name='forum-question_answers'),
    url(r'^topics/(?P<pk>\d+)/questions/(?P<ques_pk>\d+)/reply/$', views.ques_reply, name='forum-question_reply'),
    url(r'^topics/(?P<pk>\d+)/questions/(?P<ques_pk>\d+)/ans/(?P<ans_pk>\d+)/edit/$', views.ReplyUpdateView.as_view(), name='edit_post'),
]
