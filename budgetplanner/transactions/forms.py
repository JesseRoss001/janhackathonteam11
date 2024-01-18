from django import forms


from .models import Expense, TypicalExpense, Income, TypicalIncome,Budget
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

class BudgetForm(forms.ModelForm):
    total_budget = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=0, 
        help_text='Enter your total budget. Only two decimal places are allowed.',
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    savings_goal = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=0, 
        required=False, 
        help_text='Enter your savings goal (optional). Only two decimal places are allowed.',
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select the start date for the budget.'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select the end date for the budget.'
    )

    class Meta:
        model = Budget
        fields = ['total_budget', 'savings_goal', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date should be after the start date.')

        return cleaned_data

    def clean_total_budget(self):
        total_budget = self.cleaned_data['total_budget']
        if total_budget < 0:
            raise forms.ValidationError("The total budget cannot be negative.")
        return total_budget

    def clean_savings_goal(self):
        savings_goal = self.cleaned_data.get('savings_goal')
        if savings_goal is not None and savings_goal < 0:
            raise forms.ValidationError("The savings goal cannot be negative.")
        return savings_goal
class ExpenseForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=0, 
        help_text='Enter a positive amount. Only two decimal places are allowed.',
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    description = forms.CharField(
        max_length=50, 
        help_text='Maximum 50 characters.',
        widget=forms.TextInput(attrs={'placeholder': 'Description'})
    )

    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date', 'typical_expense']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['typical_expense'].queryset = TypicalExpense.objects.all()
        self.fields['typical_expense'].empty_label = "Select a typical expense"

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount and amount.as_tuple().exponent < -2:
            raise ValidationError('Enter an amount with up to two decimal places.')
        return amount

class IncomeForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        help_text='Enter a positive amount. Only two decimal places are allowed.',
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    source = forms.CharField(
        max_length=100,
        help_text='Enter the source of the income.',
        widget=forms.TextInput(attrs={'placeholder': 'Source'})
    )

    class Meta:
        model = Income
        fields = ['amount', 'source', 'date','typical_income']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['typical_income'].queryset = TypicalIncome.objects.all()
            self.fields['typical_income'].empty_label = "Select a typical income"
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError("The amount cannot be negative.")
        return amount