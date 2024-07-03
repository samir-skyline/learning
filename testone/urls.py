from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list ,name="student_list"),
    path('add/', views.create ,name="create_student"),
    path('update/', views.update ,name="update_student"),
    path('delete/', views.delete ,name="delete_student"),
]
