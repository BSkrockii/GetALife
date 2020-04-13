from django import forms
from .models import *
from django.forms import ModelForm, DateInput

# put forms here

class budgetAccountForm(forms.ModelForm):
    class Meta:
        model = Budget_account
        fields = ('users','name', 'description')

class ExpenseTypeForm(forms.ModelForm):
    class Meta:
        model = Expense_type
        fields = ('name', 'description')

class IncomeTypeForm(forms.ModelForm):
    class Meta:
        model = Income_type
        fields = ('name', 'description')

class BudgetExpenseForm(forms.ModelForm):
    class Meta:
        model = Budget_expense
        fields = ('name', 'description', 'account', 'expenseType', 'month', 'expense')

class BudgetIncomeForm(forms.ModelForm):
    class Meta:
        model = Budget_income
        fields = ('name', 'description', 'account', 'incomeType', 'month', 'income')

class BudgetConfigForm(forms.ModelForm):
    class Meta:
        model = Budget_config
        fields = ('name', 'description', 'budget_limit', 'account', 'month')
        