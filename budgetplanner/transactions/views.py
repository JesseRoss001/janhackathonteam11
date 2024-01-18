from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import ExpenseForm, IncomeForm
from .models import Expense, Income
from datetime import datetime, timedelta
from decimal import Decimal


@login_required
def income_view(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Income added successfully!')
            return redirect('income')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = IncomeForm()

    # Calculate totals similarly as we did for expenses
    today = datetime.today()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    monthly_income_total = Income.objects.filter(
        user=request.user,
        date__gte=start_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    yearly_income_total = Income.objects.filter(
        user=request.user,
        date__gte=start_of_year
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    incomes = Income.objects.filter(user=request.user).order_by('-date')
    datewise_totals = incomes.values('date').annotate(
        total=Sum('amount')).order_by('-date')

    context = {
        'form': form,
        'incomes': incomes,
        'monthly_income_total': monthly_income_total,
        'yearly_income_total': yearly_income_total,
    }

    return render(request, 'transactions/income.html', context)


@login_required
def expenditure_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expenditure')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExpenseForm()

    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    datewise_totals = expenses.values('date').annotate(
        total=Sum('amount')).order_by('-date')

    # Get current date and calculate the start of the week, month, and year
    current_date = now().date()
    start_of_week = current_date - \
        timedelta(days=current_date.weekday()) + timedelta(days=3)
    start_of_month = current_date.replace(day=1)
    start_of_year = current_date.replace(month=1, day=1)

    # Adjust the start_of_week if it's in the future
    if start_of_week > current_date:
        start_of_week -= timedelta(weeks=1)

    # Aggregate expenses
    weekly_totals = expenses.filter(
        date__gte=start_of_week).aggregate(weekly_total=Sum('amount'))
    monthly_totals = expenses.filter(
        date__gte=start_of_month).aggregate(monthly_total=Sum('amount'))
    yearly_totals = expenses.filter(
        date__gte=start_of_year).aggregate(yearly_total=Sum('amount'))

    # Calculate daily totals for the current week
    daily_totals = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        total = expenses.filter(date=day).aggregate(
            total=Sum('amount'))['total'] or 0
        daily_totals.append({'day': day, 'total': total})

    context = {
        'form': form,
        'expenses': expenses,
        'datewise_totals': datewise_totals,
        'weekly_totals': weekly_totals,
        'monthly_totals': monthly_totals,
        'yearly_totals': yearly_totals,
        'daily_totals': daily_totals,
    }

    return render(request, 'transactions/expenditure.html', context)

# views.py


def reports_view(request):
    return render(request, 'transactions/reports.html')

# Create your views here.
