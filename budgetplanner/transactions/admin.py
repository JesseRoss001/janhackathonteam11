from django.contrib import admin
from .models import WeeklyBudget, MonthlyBudget, YearlyBudget, Expense, Income

admin.site.register(WeeklyBudget)
admin.site.register(MonthlyBudget)
admin.site.register(YearlyBudget)
admin.site.register(Expense)
admin.site.register(Income)

# Register your models here.
