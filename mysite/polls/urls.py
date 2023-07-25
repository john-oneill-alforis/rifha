from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashBoard"),
    path("trainingcorpus/", views.contentList, name="contentList"),
    path("content/<str:msg>", views.contentReview, name="article"),
    path("tcupdate/<str:msg>", views.tcUpdate, name="tcUpdate"),
    path("verisData/", views.verisDashboard, name="verisDashboard"),
    path("debugData/", views.debugDashboard, name="debugDashboard"),
    path("verisaro/", views.verisaro, name="verisaro"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("home/", views.dashboard, name="home"),
    path("errors/", views.errorLog, name="errors"),
    path("interviewStats/", views.get_interviewStats, name="interviewStats"),
    path("createInterviewee/", views.get_createInterviewee, name="createInterviewee"),
    path(
        "createInterviewQuestion/",
        views.get_interviewQuestion,
        name="createInterviewee",
    ),
    path(
        "createInterviewResponses/",
        views.get_interviewResponses,
        name="createInterviewResponses",
    ),
    path(
        "listInterviewee/",
        views.get_interviewees,
        name="listInterviewee",
    ),


    
]
