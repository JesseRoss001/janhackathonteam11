from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from .forms import UserRegistrationForm
from .models import UserProfile
from transactions.models import WeeklyBudget, MonthlyBudget, YearlyBudget, Expense, Income
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
from transactions.models import get_income_totals, get_expense_totals

from django.contrib.auth import authenticate, login


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        # Get username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            # Log the user in
            login(request, user)
            # Redirect to the dashboard view
            return redirect(reverse('dashboard'))
        else:
            # Return an 'invalid login' error message
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        # Render the login form template if not a POST request
        return render(request, 'login.html')


def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt'
            )

            # In preparation for when we add toast messages
            messages.success(
                request, 'Instructions to reset your password have been sent to your email.')
            messages.error(
                request, 'An error occurred while sending the email. Please try again later.')

            return redirect(reverse('login'))
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset.html', {'form': form})


def dashboard_view(request):
    context = {}
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            context['user_profile'] = user_profile
            context['current_balance'] = user_profile.current_balance()
            context.update(get_income_totals(request.user))
            context.update(get_expense_totals(request.user))
            context = {
        'weekly_income_total': weekly_income_total,
        'monthly_income_total': monthly_income_total,
        'yearly_income_total': yearly_income_total,
        'weekly_expenditure_total': weekly_expenditure_total,
        'monthly_expenditure_total': monthly_expenditure_total,
        'yearly_expenditure_total': yearly_expenditure_total,
        # ... other context variables
        }
        except UserProfile.DoesNotExist:
            context['user_profile'] = None
        
    return render(request, 'dashboard.html', context)


def faq_view(request):
    return render(request, 'faq.html')


def contact_view(request):
    return render(request, 'contact.html')


def about_view(request):
    return render(request, 'about.html')
