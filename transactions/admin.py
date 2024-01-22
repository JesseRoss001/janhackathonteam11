from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    User, DebtDetail, ExpenseCategory, IncomeCategory, Income,
    WeeklyBudget, MonthlyBudget, YearlyBudget, Expense, SavingsInvestment
)

# Admin class for DebtDetail
class DebtDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'debt_name', 'amount', 'interest_rate', 'interest_type', 'last_updated')
    list_filter = ('user', 'interest_type')
    search_fields = ['user__username', 'debt_name']
    ordering = ('-last_updated',)

# Admin class for ExpenseCategory
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name', ]

# Admin class for IncomeCategory
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name', ]

# Admin class for Income
class IncomeAdmin(SummernoteModelAdmin):
    list_display = ('user', 'amount', 'source', 'date', 'category')
    list_filter = ('date', 'category')
    search_fields = ['user__username', 'source']
    summernote_fields = ('source')
    ordering = ('-date',)

# Admin class for Budget (Abstract class)
# No admin registration needed for abstract models

# Admin class for WeeklyBudget
class WeeklyBudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'start_date', 'end_date', 'description')
    list_filter = ('user', 'start_date')
    search_fields = ['user__username', 'description']
    ordering = ('-start_date',)

# Admin class for MonthlyBudget
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'start_date', 'end_date', 'description')
    list_filter = ('user', 'start_date')
    search_fields = ['user__username', 'description']
    ordering = ('-start_date',)

# Admin class for YearlyBudget
class YearlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'start_date', 'end_date', 'description')
    list_filter = ('user', 'start_date')
    search_fields = ['user__username', 'description']
    ordering = ('-start_date',)

# Admin class for Expense
class ExpenseAdmin(SummernoteModelAdmin):
    list_display = ('user', 'amount', 'description', 'date', 'category')
    list_filter = ('date', 'category')
    search_fields = ['user__username', 'description']
    summernote_fields = ('description')
    ordering = ('-date',)

# Admin class for SavingsInvestment
class SavingsInvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'investment_type', 'date_created', 'last_updated', 'best_case_return', 'worst_case_return')
    list_filter = ('investment_type', 'date_created')
    search_fields = ['user__username']
    ordering = ('-date_created',)

# Register your models here
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(DebtDetail, DebtDetailAdmin)
admin.site.register(WeeklyBudget, WeeklyBudgetAdmin)
admin.site.register(MonthlyBudget, MonthlyBudgetAdmin)
admin.site.register(YearlyBudget, YearlyBudgetAdmin)
admin.site.register(SavingsInvestment, SavingsInvestmentAdmin)
