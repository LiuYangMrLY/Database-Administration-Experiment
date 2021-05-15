"""db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path('get_students', views.get_students),
    path('add_student', views.add_student),
    path('delete_student', views.delete_student),
    path('edit_student', views.edit_student),
    path('search_student', views.search_student),

    path('get_courses', views.get_courses),
    path('add_course', views.add_course),
    path('delete_course', views.delete_course),
    path('edit_course', views.edit_course),
    path('search_course', views.search_course),

    path('get_sc', views.get_sc),
    path('add_sc', views.add_sc),
    path('delete_sc', views.delete_sc),
    path('edit_sc', views.edit_sc),
    path('search_sc', views.search_sc),
]
