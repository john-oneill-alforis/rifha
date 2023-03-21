from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("content/<str:msg>", views.contentReview, name="article"),
    path("tcupdate/<str:msg>", views.tcUpdate, name="tcUpdate"),
]
