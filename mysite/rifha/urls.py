from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashBoard"),
    path("assets/", views.assetsHome, name="assetsHome"),
    path("people/", views.peopleHome, name="peopleHome"),
    path("peopleEdit/<str:msg>/", views.peopleEdit, name="peopleEdit"),
    path("peopleAdd/", views.peopleAdd, name="peopleAdd"),
    path("admin/", views.admin, name="admin"),
    path("addClassification/", views.classificationAdd, name="classificationAdd"),
    path("classificationEdit/<str:msg>/", views.classificationEdit, name="peopleEdit"),
]
