from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import ExpenseForm, IncomeForm 
from .models import Expense, Income
from .models import WeeklyBudget, MonthlyBudget, YearlyBudget
from .forms import WeeklyBudgetForm, MonthlyBudgetForm, YearlyBudgetForm
from datetime import datetime, timedelta
from decimal import Decimal

@login_required
def manage_budgets(request):
    user = request.user
    current_date = now().date()

    # Fetch existing budgets
    weekly_budgets = WeeklyBudget.objects.filter(user=user)
    monthly_budgets = MonthlyBudget.objects.filter(user=user, month__year=current_date.year)
    yearly_budgets = YearlyBudget.objects.filter(user=user, year__year=current_date.year)

    # Initialize forms
    weekly_form = WeeklyBudgetForm()
    monthly_form = MonthlyBudgetForm()
    yearly_form = YearlyBudgetForm()

    if request.method == 'POST':
        # Handle creation of budgets
        if 'create_weekly' in request.POST:
            weekly_form = WeeklyBudgetForm(request.POST)
            if weekly_form.is_valid():
                weekly_budget = weekly_form.save(commit=False)
                weekly_budget.user = user
                weekly_budget.save()
                messages.success(request, 'Weekly budget created successfully!')
                return redirect('manage_budgets')

        elif 'create_monthly' in request.POST:
            monthly_form = MonthlyBudgetForm(request.POST)
            if monthly_form.is_valid():
                monthly_budget = monthly_form.save(commit=False)
                monthly_budget.user = user
                monthly_budget.save()
                messages.success(request, 'Monthly budget created successfully!')
                return redirect('manage_budgets')

        elif 'create_yearly' in request.POST:
            yearly_form = YearlyBudgetForm(request.POST)
            if yearly_form.is_valid():
                yearly_budget = yearly_form.save(commit=False)
                yearly_budget.user = user
                yearly_budget.save()
                messages.success(request, 'Yearly budget created successfully!')
                return redirect('manage_budgets')

        # Handle updating of budgets
        elif 'update_weekly' in request.POST:
            budget_id = request.POST.get('budget_id')
            budget_instance = get_object_or_404(WeeklyBudget, id=budget_id, user=user)
            weekly_form = WeeklyBudgetForm(request.POST, instance=budget_instance)
            if weekly_form.is_valid():
                weekly_form.save()
                messages.success(request, 'Weekly budget updated successfully!')
                return redirect('manage_budgets')

        elif 'update_monthly' in request.POST:
            budget_id = request.POST.get('budget_id')
            budget_instance = get_object_or_404(MonthlyBudget, id=budget_id, user=user)
            monthly_form = MonthlyBudgetForm(request.POST, instance=budget_instance)
            if monthly_form.is_valid():
                monthly_form.save()
                messages.success(request, 'Monthly budget updated successfully!')
                return redirect('manage_budgets')

        elif 'update_yearly' in request.POST:
            budget_id = request.POST.get('budget_id')
            budget_instance = get_object_or_404(YearlyBudget, id=budget_id, user=user)
            yearly_form = YearlyBudgetForm(request.POST, instance=budget_instance)
            if yearly_form.is_valid():
                yearly_form.save()
                messages.success(request, 'Yearly budget updated successfully!')
                return redirect('manage_budgets')

        # Handle deletion of budgets
        elif 'delete_weekly' in request.POST:
            budget_id = request.POST.get('budget_id')
            budget_instance = get_object_or_404(WeeklyBudget, id=budget_id, user=user)
            budget_instance.delete()
            messages.success(request, 'Weekly budget deleted successfully!')
            return redirect('manage_budgets')

        elif 'delete_monthly' in request.POST:
            budget_id = request.POST.get('budget_id')
            budget_instance = get_object_or_404(MonthlyBudget, id=budget_id, user=user)
            budget_instance.delete()
            messages.success(request, 'Monthly budget deleted successfully!')
            return redirect('manage_budgets')

        elif 'delete_yearly' in request.POST:
            budget_id = request.POST.get('budget_id')
            budget_instance = get_object_or_404(YearlyBudget, id=budget_id, user=user)
            budget_instance.delete()
            messages.success(request, 'Yearly budget deleted successfully!')
            return redirect('manage_budgets')

    # Render the template with forms and existing budgets
    context = {
        'weekly_budgets': weekly_budgets,
        'monthly_budgets': monthly_budgets,
        'yearly_budgets': yearly_budgets,
        'weekly_form': weekly_form,
        'monthly_form': monthly_form,
        'yearly_form': yearly_form
    }
    return render(request, 'transactions/manage_budgets.html', context)
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
    datewise_totals = incomes.values('date').annotate(total=Sum('amount')).order_by('-date')

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
    datewise_totals = expenses.values('date').annotate(total=Sum('amount')).order_by('-date')

    # Get current date and calculate the start of the week, month, and year
    current_date = now().date()
    start_of_week = current_date - timedelta(days=current_date.weekday()) + timedelta(days=3)
    start_of_month = current_date.replace(day=1)
    start_of_year = current_date.replace(month=1, day=1)

    # Adjust the start_of_week if it's in the future
    if start_of_week > current_date:
        start_of_week -= timedelta(weeks=1)

    # Aggregate expenses
    weekly_totals = expenses.filter(date__gte=start_of_week).aggregate(weekly_total=Sum('amount'))
    monthly_totals = expenses.filter(date__gte=start_of_month).aggregate(monthly_total=Sum('amount'))
    yearly_totals = expenses.filter(date__gte=start_of_year).aggregate(yearly_total=Sum('amount'))
    
    # Calculate daily totals for the current week
    daily_totals = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        total = expenses.filter(date=day).aggregate(total=Sum('amount'))['total'] or 0
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
@login_required
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expenditure')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'transactions/update_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expenditure')
    return render(request, 'transactions/delete_expense.html', {'expense': expense})
def reports_view(request):
    return render(request, 'transactions/reports.html')

# Create your views here.
@login_required
def update_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully!')
            return redirect('income')  # Replace with your view name
    else:
        form = IncomeForm(instance=income)
    return render(request, 'transactions/update_income.html', {'form': form})

@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully!')
        return redirect('income')  # Replace with your view name
    return render(request, 'transactions/delete_income.html', {'income': income})