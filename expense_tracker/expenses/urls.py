from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.Login,name="Login"),
    path('home/', views.view_expenses, name="view_expenses"),
    path('edit/<int:id>/', views.edit_expense, name="edit_expense"),
    path('delete/<int:id>/', views.delete_expense, name="delete_expense"),
    path('dashboard/', views.dashboard, name="dashboard"),
]
