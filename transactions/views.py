from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import ExpenseForm, IncomeForm
from .models import Expense, Income
from datetime import datetime, timedelta
from datetime import date
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from .models import WeeklyBudget, MonthlyBudget, YearlyBudget,DebtDetail
from .forms import WeeklyBudgetForm, MonthlyBudgetForm, YearlyBudgetForm,DebtDetailForm
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Min
from django.forms.widgets import SelectDateWidget
#Premium Features


@login_required
def manage_debts(request):
    user = request.user
    starting_debt = UserProfile.objects.get(user=user).indebt  # Replace with actual field name
    debts = DebtDetail.objects.filter(user=user)
    total_current_debts = sum(debt.amount for debt in debts)

    context = {
        'debts': debts,
        'starting_debt': starting_debt,
        'total_current_debts': total_current_debts
    }
    return render(request, 'transactions/debts.html', context)

@login_required
def add_edit_debt(request, debt_id=None):
    user = request.user
    if debt_id:
        debt = get_object_or_404(DebtDetail, id=debt_id, user=user)
    else:
        debt = None

    if request.method == 'POST':
        form = DebtDetailForm(request.POST, instance=debt)
        if form.is_valid():
            new_debt = form.save(commit=False)
            new_debt.user = user
            new_debt.save()
            messages.success(request, 'Debt detail added/updated successfully!')
            return redirect('manage_debts')
    else:
        form = DebtDetailForm(instance=debt)

    return render(request, 'transactions/add_edit_debt.html', {'form': form, 'debt': debt})

@login_required
def delete_debt(request, debt_id):
    debt = get_object_or_404(DebtDetail, id=debt_id, user=request.user)
    if request.method == 'POST':
        debt.delete()
        messages.success(request, 'Debt deleted successfully!')
        return redirect('manage_debts')
    return render(request, 'transactions/delete_debt.html', {'debt': debt})

@login_required
def update_budget(request, budget_id, budget_type):
    BudgetModel = {
        'weekly': WeeklyBudget,
        'monthly': MonthlyBudget,
        'yearly': YearlyBudget
    }.get(budget_type)

    budget = get_object_or_404(BudgetModel, id=budget_id, user=request.user)

    if request.method == 'POST':

        form = {
            'weekly': WeeklyBudgetForm,
            'monthly': MonthlyBudgetForm,
            'yearly': YearlyBudgetForm
        }.get(budget_type)(request.POST, instance=budget)

        if form.is_valid():
            form.save()
            messages.success(
                request, f'{budget_type.capitalize()} budget updated successfully!')
            return redirect('manage_budgets')
    else:
        form = {
            'weekly': WeeklyBudgetForm,
            'monthly': MonthlyBudgetForm,
            'yearly': YearlyBudgetForm
        }.get(budget_type)(instance=budget)

    return render(request, 'transactions/update_budget.html', {'form': form, 'budget_type': budget_type})


@login_required
def manage_budgets(request):
    user = request.user

    weekly_budgets = WeeklyBudget.objects.filter(user=user)
    monthly_budgets = MonthlyBudget.objects.filter(user=user)
    yearly_budgets = YearlyBudget.objects.filter(user=user)

    if request.method == 'POST':
        # Handling Weekly Budget Form
        if 'weekly_budget' in request.POST:
            weekly_form = WeeklyBudgetForm(request.POST)
            if weekly_form.is_valid():
                weekly_budget = weekly_form.save(commit=False)
                weekly_budget.user = user
                # Check for overlapping budgets
                if not WeeklyBudget.objects.filter(user=user, start_date=weekly_budget.start_date).exists():
                    weekly_budget.save()
                    messages.success(
                        request, 'Weekly budget created successfully!')
                else:
                    messages.error(
                        request, 'A weekly budget for this period already exists.')
            else:
                messages.error(
                    request, 'Please correct the errors in the weekly budget form.')

        # Handling delete request for Weekly Budget
        elif 'delete_weekly' in request.POST:
            budget_id = request.POST.get('budget_id')
            WeeklyBudget.objects.filter(id=budget_id, user=user).delete()
            messages.success(request, 'Weekly budget deleted successfully!')

        # Handling Monthly Budget Form
        elif 'monthly_budget' in request.POST:
            monthly_form = MonthlyBudgetForm(request.POST)
            if monthly_form.is_valid():
                monthly_budget = monthly_form.save(commit=False)
                monthly_budget.user = user
                if not MonthlyBudget.objects.filter(user=user, start_date=monthly_budget.start_date).exists():
                    monthly_budget.save()
                    messages.success(
                        request, 'Monthly budget created successfully!')
                else:
                    messages.error(
                        request, 'A monthly budget for this period already exists.')
            else:
                messages.error(
                    request, 'Please correct the errors in the monthly budget form.')

        # Handling delete request for Monthly Budget
        elif 'delete_monthly' in request.POST:
            budget_id = request.POST.get('budget_id')
            MonthlyBudget.objects.filter(id=budget_id, user=user).delete()
            messages.success(request, 'Monthly budget deleted successfully!')

        # Handling Yearly Budget Form
        elif 'yearly_budget' in request.POST:
            yearly_form = YearlyBudgetForm(request.POST)
            if yearly_form.is_valid():
                yearly_budget = yearly_form.save(commit=False)
                yearly_budget.user = user
                if not YearlyBudget.objects.filter(user=user, start_date=yearly_budget.start_date).exists():
                    yearly_budget.save()
                    messages.success(
                        request, 'Yearly budget created successfully!')
                else:
                    messages.error(
                        request, 'A yearly budget for this period already exists.')
            else:
                messages.error(
                    request, 'Please correct the errors in the yearly budget form.')

        # Handling delete request for Yearly Budget
        elif 'delete_yearly' in request.POST:
            budget_id = request.POST.get('budget_id')
            YearlyBudget.objects.filter(id=budget_id, user=user).delete()
            messages.success(request, 'Yearly budget deleted successfully!')

        return redirect('manage_budgets')

    else:
        weekly_form = WeeklyBudgetForm()
        monthly_form = MonthlyBudgetForm()
        yearly_form = YearlyBudgetForm()

    context = {
        'weekly_budgets': weekly_budgets,
        'monthly_budgets': monthly_budgets,
        'yearly_budgets': yearly_budgets,
        'weekly_form': weekly_form,
        'monthly_form': monthly_form,
        'yearly_form': yearly_form,
    }
    return render(request, 'transactions/manage_budgets.html', context)


def calculate_start_date():
    # Calculate the start date (Thursday of the current week)
    current_date = now().date()
    start_date = current_date + timedelta((3 - current_date.weekday() + 7) % 7)
    return start_date


def handle_budget_update_delete(request, budget_id, BudgetModel, budget_form, budget_type):
    budget_instance = get_object_or_404(
        BudgetModel, id=budget_id, user=request.user)
    if 'update_' + budget_type in request.POST:
        budget_form = budget_form.__class__(
            request.POST, instance=budget_instance)
        if budget_form.is_valid():
            budget_form.save()
            messages.success(
                request, f'{budget_type.capitalize()} budget updated successfully!')

    return redirect('manage_budgets')


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


@login_required
def reports_view(request):
    user = request.user
    today = datetime.today().date()  # Ensure today is a date object

    budget_data = []
    for budget_model in [WeeklyBudget, MonthlyBudget, YearlyBudget]:
        budgets = budget_model.objects.filter(user=user)

        for budget in budgets:
            elapsed_days, total_days, progress_percentage = calculate_budget_progress(
                budget, today)
            income_total = get_period_total(budget, Income)
            expense_total = get_period_total(budget, Expense)
            surplus_deficit = income_total - expense_total
            budget_health, budget_comment = calculate_budget_health(
                budget, elapsed_days, total_days, income_total, expense_total)

            budget_data.append({
                'type': budget_model.__name__.replace('Budget', ''),
                'amount': budget.amount,
                'start_date': budget.start_date,
                'end_date': budget.end_date,
                'progress': progress_percentage,
                'health': budget_health,
                'comment': budget_comment,
                'income_total': income_total,
                'expense_total': expense_total,
                'surplus_deficit': surplus_deficit,
            })

    context = {
        'budget_data': budget_data,
    }

    return render(request, 'transactions/reports.html', context)

# Helper functions below


def calculate_budget_progress(budget, today_date):
    start_date = budget.start_date
    end_date = budget.end_date or today_date
    total_days = (end_date - start_date).days
    elapsed_days = (
        today_date - start_date).days if today_date >= start_date else 0
    progress_percentage = min(
        (elapsed_days / total_days * 100), 100) if total_days > 0 else 0
    return elapsed_days, total_days, progress_percentage


def calculate_budget_health(budget, elapsed_days, total_days, income_for_period, expense_for_period):
    budget_amount = budget.amount or Decimal('0.00')
    progress_percentage = calculate_budget_progress(
        budget, datetime.today().date())[2]

    if income_for_period == Decimal('0.00'):
        budget_health = 'bad'
        budget_comment = 'Income not updated'
    elif progress_percentage >= 100:
        if expense_for_period <= budget_amount:
            budget_health = 'completed-success'
            budget_comment = 'Budget period completed successfully'
        else:
            budget_health = 'completed-failure'
            budget_comment = 'Budget period completed, over budget'
    elif expense_for_period <= budget_amount:
        budget_health = 'good'
        budget_comment = 'On track'
    else:
        budget_health = 'poor'
        budget_comment = 'Over budget'

    return budget_health, budget_comment


def get_period_total(budget, model):
    """
    Calculate the total amount of a given model (Income or Expense) for the budget's period.
    """
    if model not in [Income, Expense]:
        raise ValueError("Model must be either Income or Expense")

    # Check if the budget has an end date, use today's date if not.
    end_date = budget.end_date if budget.end_date else datetime.today().date()

    # Aggregate the total amount for the specified period.
    total = model.objects.filter(
        user=budget.user,
        date__gte=budget.start_date,
        date__lte=end_date
    ).aggregate(total_amount=Sum('amount'))['total_amount']

    return total if total else Decimal('0.00')


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
    return render(request, 'transactions/update_income.html', {'form': form, 'income': income})


@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully!')
        return redirect('income')  # Replace with your view name
    return render(request, 'transactions/delete_income.html', {'income': income})
