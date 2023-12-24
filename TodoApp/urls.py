from django.urls import path
from TodoApp import views

urlpatterns = [
    path('<int:id>/', views.TodoListCreateApiView.as_view(), name='notice-detail-view'),
]
