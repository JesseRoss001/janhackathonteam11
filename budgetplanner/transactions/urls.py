from django.urls import path
from . import views

urlpatterns = [
    path('income/', views.income_view, name='income'),
    path('expenditure/', views.expenditure_view, name='expenditure'),
    
    path('reports/', views.reports_view, name='reports'),
    path('budget/', views.budget_view, name='budget'),
     path('expenses/update/<int:expense_id>/', views.update_expense, name='update_expense'),
    path('expenses/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]