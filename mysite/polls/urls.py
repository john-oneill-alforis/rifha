from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashBoard"),
    path("trainingcorpus", views.contentList, name="contentList"),
    path("content/<str:msg>", views.contentReview, name="article"),
    path("tcupdate/<str:msg>", views.tcUpdate, name="tcUpdate"),
    path("verisData", views.verisDashboard, name="verisDashboard"),
    path("debugData", views.debugDashboard, name="debugDashboard"),
]
