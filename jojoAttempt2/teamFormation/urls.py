from django.urls import path
from . import views


urlpatterns = [
    path('', views.uploadFile, name="home"),
    path('test-delete/', views.test_delete, name='test_delete'),
    path('test-session/', views.test_session, name='test_session'),
    path('save-session-data/', views.save_session_data, name='save_session_data'),
    path('access-session-data/', views.access_session_data, name='access_session_data'),
    path('delete-session-data/', views.delete_session_data, name='delete_session_data'),
    path('columns/', views.pickColumns, name="columns"),
]