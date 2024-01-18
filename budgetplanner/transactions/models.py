# transactions/models.py
from django.db import models
from accounts.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils.timezone import now
from decimal import Decimal
class TypicalExpense(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Function to create typical expenses
def create_typical_expenses():
    TypicalExpense.objects.create(name='Rent')
    TypicalExpense.objects.create(name='Car Insurance')
    TypicalExpense.objects.create(name='Groceries')
    TypicalExpense.objects.create(name='Utilities')
    TypicalExpense.objects.create(name='Health Insurance')
    TypicalExpense.objects.create(name='Internet Bill')
    TypicalExpense.objects.create(name='Dining Out')
    TypicalExpense.objects.create(name='Electricity Bill')
    TypicalExpense.objects.create(name='Gas Bill')
    TypicalExpense.objects.create(name='Water Bill')
    TypicalExpense.objects.create(name='Phone Bill')
    TypicalExpense.objects.create(name='Transportation')
    TypicalExpense.objects.create(name='Clothing')
    TypicalExpense.objects.create(name='Entertainment')
    TypicalExpense.objects.create(name='Gym Membership')
    TypicalExpense.objects.create(name='Childcare')
    TypicalExpense.objects.create(name='Education')
    TypicalExpense.objects.create(name='Healthcare')
    TypicalExpense.objects.create(name='Home Repairs')
    TypicalExpense.objects.create(name='Travel')
    TypicalExpense.objects.create(name='Gifts')
    TypicalExpense.objects.create(name='Pet Expenses')
    TypicalExpense.objects.create(name='Charity Donations')
    TypicalExpense.objects.create(name='Hobbies')
    TypicalExpense.objects.create(name='Taxes')
    TypicalExpense.objects.create(name='Insurance Premiums')
    TypicalExpense.objects.create(name='Subscription Services')
    TypicalExpense.objects.create(name='Home Maintenance')

class TypicalIncome(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
def create_typical_incomes():
    TypicalIncome.objects.create(name='Salary')
    TypicalIncome.objects.create(name='Bonus')

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    date = models.DateField()
    typical_income = models.ForeignKey(TypicalIncome, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s income from {self.source} on {self.date}"


class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add any additional fields as necessary

    def __str__(self):
        return f"{self.user.username}'s savings"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s budget from {self.start_date} to {self.end_date}"

    def update_budget_balance(self):
        total_income = Income.objects.filter(user=self.user).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        total_expense = Expense.objects.filter(user=self.user).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        self.budget_balance = total_income - total_expense
        self.save()
    def predict_future_budget(self, months=1):
        # Your logic to predict future budget
        pass

    def budget_health(self):
        total_income = Income.objects.filter(user=self.user).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        total_expense = Expense.objects.filter(user=self.user).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

        if total_income > 0:
            health_ratio = total_expense / total_income
            if health_ratio < 1:
                return "Healthy"
            elif health_ratio == 1:
                return "Balanced"
            else:
                return "Overspending"
        else:
            return "No Income Data"

    def savings_progress(self):
        total_savings = self.user.savings.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        if self.savings_goal and self.savings_goal > 0:
            progress_percentage = (total_savings / self.savings_goal) * 100
            return min(progress_percentage, 100)  # Cap at 100%
        else:
            return 0
# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50)
    date = models.DateField()
    typical_expense = models.ForeignKey(TypicalExpense, on_delete=models.SET_NULL, null=True, blank=True)

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
    start_of_week = current_date - timedelta(days=current_date.weekday()) + timedelta(days=3)
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