from django.urls import path
from . import views

urlpatterns = [
    path('', views.multiFormSubmission.as_view(), name="home"),
]