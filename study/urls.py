from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('notes/new/', views.note_create, name='note_create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # Add login view
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('logout/', views.signup, name='signup'),
]
