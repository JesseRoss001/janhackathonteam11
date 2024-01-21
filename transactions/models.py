# transactions/models.py
from django.db import models
from accounts.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils.timezone import now
from decimal import Decimal
from datetime import date
#Premuim Features 


class DebtDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debt_name = models.CharField(max_length=100)  # Changed from category to debt_name
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Annual percentage rate
    interest_type = models.CharField(max_length=10, choices=(('monthly', 'Monthly'), ('yearly', 'Yearly')))
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s debt: {self.debt_name}"

    def calculate_interest(self, current_date=date.today()):
        # Calculate the number of periods (months or years) since last update
        if self.interest_type == 'monthly':
            periods = (current_date.year - self.last_updated.year) * 12 + current_date.month - self.last_updated.month
            monthly_rate = Decimal(self.interest_rate) / Decimal(100) / Decimal(12)  # Convert annual rate to monthly
            return self.amount * (1 + monthly_rate) ** periods
        else:
            years = current_date.year - self.last_updated.year
            annual_rate = Decimal(self.interest_rate) / Decimal(100)
            return self.amount * (1 + annual_rate) ** years






















class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Expense Categories'


class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Income Categories'


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    date = models.DateField()
    category = models.ForeignKey(
        IncomeCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}'s income from {self.source} on {self.date}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username}'s budget from {self.start_date}"


class WeeklyBudget(Budget):
    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timedelta(days=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return super().__str__() + f" to {self.end_date}"


class MonthlyBudget(Budget):
    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return super().__str__() + f" to {self.end_date}"


class YearlyBudget(Budget):
    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

    def __str__(self):
        return super().__str__() + f" to {self.end_date}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50)
    date = models.DateField()
    category = models.ForeignKey(
        ExpenseCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}'s expense on {self.date}"


def get_income_totals(user):
    today = datetime.today()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    monthly_total = Income.objects.filter(
        user=user,
        date__gte=start_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    yearly_total = Income.objects.filter(
        user=user,
        date__gte=start_of_year
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    return {
        'monthly_income_total': monthly_total,
        'yearly_income_total': yearly_total
    }


def get_expense_totals(user):
    current_date = now().date()
    start_of_week = current_date - \
        timedelta(days=current_date.weekday()) + timedelta(days=3)
    start_of_month = current_date.replace(day=1)
    start_of_year = current_date.replace(month=1, day=1)

    if start_of_week > current_date:
        start_of_week -= timedelta(weeks=1)

    weekly_total = Expense.objects.filter(
        user=user, date__gte=start_of_week
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    monthly_total = Expense.objects.filter(
        user=user, date__gte=start_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    yearly_total = Expense.objects.filter(
        user=user, date__gte=start_of_year
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    return {
        'weekly_expense_total': weekly_total,
        'monthly_expense_total': monthly_total,
        'yearly_expense_total': yearly_total
    }
