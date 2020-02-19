from django.conf import settings
from django.db import models
from datetime import date

# models:
class Month(models.IntegerChoices):
    January = 0
    February = 1
    March = 2
    April = 3
    May = 4
    June = 5
    July = 6
    August = 7
    September = 8 
    October = 9
    November = 10
    December = 11

# financial_management_budget
class Budget_account(models.Model):
    # Many-Many relationship to user model
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modefied_utc = models.DateField(auto_now=True, null=False)

# financial_management_budget_expense_type
class Expense_type(models.Model):
    name = models.CharField(max_length=50, null=False)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modefied_utc = models.DateField(auto_now=True, null=False)

# financial_management_budget_income
class Income_type(models.Model):
    name = models.CharField(max_length=50, null=False)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modefied_utc = models.DateField(auto_now=True, null=False)

# financial_management_budget_expense
class Budget_expense(models.Model):
    budget = models.ForeignKey(Budget_account, on_delete=models.CASCADE)
    expenseType = models.ForeignKey(Expense_type, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50, null=False)
    month = models.IntegerField(choices=Month.choices)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modefied_utc = models.DateField(auto_now=True, null=False)


# financial_management_budget_config
class Budget_config(models.Model):
    budget = models.ForeignKey(Budget_account, on_delete=models.CASCADE)
    month = models.IntegerField(choices=Month.choices)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modefied_utc = models.DateField(auto_now=True, null=False)