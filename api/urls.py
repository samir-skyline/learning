from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('test/1/', include('testone.urls') ),
    path('person/list/', views.getList, name="list" ),
    path('person/add/',views.create, name="create" ),
    path('person/update/', views.update, name="update"),
    path('person/delete/', views.delete,name="update"),
    path('person/register/', views.register,name="register"),
    path('person/login/', views.login,name="login"),
]
