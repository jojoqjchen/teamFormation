from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name = 'home'),
    path('team-tool-input/', views.survey_input, name = 'survey_input'),
]
