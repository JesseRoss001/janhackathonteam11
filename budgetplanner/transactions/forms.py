from django import forms


from .models import Expense, TypicalExpense, Income, TypicalIncome
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import WeeklyBudget, MonthlyBudget, YearlyBudget

class WeeklyBudgetForm(forms.ModelForm):
    class Meta:
        model = WeeklyBudget
        fields = ['amount', 'start_date', 'end_date']

class MonthlyBudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ['amount', 'month']

class YearlyBudgetForm(forms.ModelForm):
    class Meta:
        model = YearlyBudget
        fields = ['amount', 'year']
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

