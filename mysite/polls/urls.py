from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("content/<str:msg>", views.contentReview, name="article"),
]
