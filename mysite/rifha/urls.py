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
    # Risk Identification Phase
    path("riskReg/", views.riskHome, name="riskReg"),
    path("riskAdd/", views.riskAdd, name="riskAdd"),
    path("riskEdit/<str:msg>/", views.riskEdit, name="riskEdit"),
    # Risk Analysis Phase
    path("riskAnalysisAdd/<str:msg>/", views.riskAnalysisAdd, name="riskAnalysisAdd"),
    path("riskControlsAdd/<str:msg>/", views.riskControlsAdd, name="riskControlsAdd"),
    path("riskthreatAdd/<str:msg>/", views.riskthreatAdd, name="riskthreatAdd"),
    path("riskReport/<str:msg>/", views.riskReport, name="riskReport"),
    # path("riskAdd/", views.riskAdd, name="riskAdd"),
    # path("riskEdit/<str:msg>/", views.riskEdit, name="riskEdit"),
    # Threat Information
    path(
        "populateThreatInformation/",
        views.populateThreatInformation,
        name="populateThreatInformation",
    ),
    # Controls Information
    path("controls/", views.controlsHome, name="controlsHome"),
]
