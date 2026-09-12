from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('problems/', views.problems, name='problems'),
    path('problems/add/', views.add_problem, name='add_problem'),
    path('problems/delete/<int:id>/', views.delete_problem, name='delete_problem'),

    path('tasks/', views.tasks, name='tasks'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/complete/<int:id>/', views.complete_task, name='complete_task'),
    path('tasks/delete/<int:id>/', views.delete_task, name='delete_task'),
]