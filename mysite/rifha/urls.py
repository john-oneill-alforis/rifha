from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashBoard"),
    path("assets/", views.assetsHome, name="assetsHome"),
    path("people/", views.peopleHome, name="peopleHome"),
    path("peopleEdit/<str:msg>/", views.peopleEdit, name="peopleEdit"),
    path("peopleAdd/", views.peopleAdd, name="peopleAdd"),
]
