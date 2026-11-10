from django.urls import path
from . import views

app_name = 'lfg'

urlpatterns = [
    path('', views.lfg_list, name='list'),
    path('<int:pk>/', views.lfg_detail, name='detail'),
    path('create/', views.lfg_create, name='create'),
    path('<int:pk>/edit/', views.lfg_edit, name='edit'),
    path('<int:pk>/delete/', views.lfg_delete, name='delete'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/join/', views.event_join, name='event_join'),
    path('events/<int:pk>/leave/', views.event_leave, name='event_leave'),
]
