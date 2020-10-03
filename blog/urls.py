"""RGUKTN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
urlpatterns = [
    path('',views.home,name='blog-home'),
    path('home',views.home,name='blog-home'),
    path('posts',views.PostListView.as_view(),name='blog-posts'),
    path('user/<str:username>',views.UserPostListView.as_view(),name="user-posts"),
    path('post/<int:pk>',views.PostDetailView.as_view(),name="post-detail"),
    path('post/new/',views.PostCreateView.as_view(),name = "post-create"),
    path("post/<int:pk>/update",views.PostUpdateView.as_view(),name="post-update"),
    path("post/<int:pk>/delete",views.PostDeleteView.as_view(),name="post-delete"),
    path('attendence/',views.attendence,name='attendence'),
    path("settings/",views.settings,name="settings"),
    path("about/",views.about,name="about"),
    path("test/",views.test,name="test"),
    path("timetable/",views.timetable,name="timetable"),
    path("today/",views.today,name="today"),
    path("analysis/",views.analysis,name="analysis"),
    path("playlist_time",views.getTime,name="youtube_playlist"),
    path("youtube_search",views.getVideos,name="youtube_search"),
    path("pockets",views.pocket,name="pockets"),
    path("bookupload", views.bookupload , name = "bookupload"),
]
