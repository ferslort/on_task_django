"""on_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import index_page, register_page, logout_page
from project import views as project_views
from task import views as task_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index_page'),
    path('register/', register_page, name='register_page'),
    path('dashboard/', project_views.dashboard_page, name='dashboard_page'),
    path('project/create', project_views.create_project, name='create_project'),
    path('project/<id>', project_views.project_detail, name='project'),
    path('project/edit/<id>', project_views.project_edit, name='edit_project'),
    path('project/delete/<id>', project_views.project_delete, name='delete_project'),
    path('task/create/<id>', task_views.add_task, name='create_task'),
    path('task/completed/<id>', task_views.completed_task, name='completed_task'),
    path('task/delete/<id>', task_views.delete_task, name='delete_task'),
    path('task/edit/<id>', task_views.edit_task, name='edit_task'),
    path('logout/', logout_page, name='logout_page'),
]
