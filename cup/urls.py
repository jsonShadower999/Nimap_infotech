"""
URL configuration for techassignment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .views import ProjectViewSet, client_detail, client_list
from rest_framework.routers import DefaultRouter
from cup import views
router = DefaultRouter()
router.register(r'projects', ProjectViewSet) #fetch all projects related data
#,include
# from django.conf.urls import url
# from .views import client_list, client_detail, project_create, project_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', client_list), #fetch client related data
    path('clients/<int:pk>/',client_detail), #fetch single client related data
    path('loginuser/',views.login_page,name='loginuser'), # fetch details of logged in user using loginuser.html as login page 
    #gives you detail of user currently logged in with its project details
  
   # path('login/', views.login_page, name='login'),
] + router.urls
