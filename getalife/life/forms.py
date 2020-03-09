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
        

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)