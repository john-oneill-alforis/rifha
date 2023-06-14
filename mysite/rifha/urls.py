from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashBoard"),
    path("assets/", views.assettHome, name="assetsHome"),
    path("assettEdit/<str:msg>/", views.assettEdit, name="assettEdit"),
    path("assettAdd/", views.assettAdd, name="assettAdd"),
    path("people/", views.peopleHome, name="peopleHome"),
    path("peopleEdit/<str:msg>/", views.peopleEdit, name="peopleEdit"),
    path("peopleAdd/", views.peopleAdd, name="peopleAdd"),
    path("admin/", views.admin, name="admin"),
    path("addClassification/", views.classificationAdd, name="classificationAdd"),
    path("classificationEdit/<str:msg>/", views.classificationEdit, name="peopleEdit"),
    path("assettTypeAdd/", views.assettTypeAdd, name="assettTypeAdd"),
    path("assettTypeEdit/<str:msg>/", views.assettTypeEdit, name="assettTypeEdit"),
]
