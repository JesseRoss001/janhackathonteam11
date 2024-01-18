from django.urls import path
from . import views

urlpatterns = [
    path('income/', views.income_view, name='income'),
    path('expenditure/', views.expenditure_view, name='expenditure'),
    
    path('reports/', views.reports_view, name='reports'),
    path('budget/', views.budget_view, name='budget'),
]