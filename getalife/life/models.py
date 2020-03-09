from django.conf import settings
from django.db import models
from datetime import date, datetime
from django.urls import reverse

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

# budget
class Budget_account(models.Model):
    # Many-Many relationship to user model
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modified_utc = models.DateField(auto_now=True, null=False)

# budget_expense_type
class Expense_type(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modified_utc = models.DateField(auto_now=True, null=False)

# budget_income_type
class Income_type(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modified_utc = models.DateField(auto_now=True, null=False)

# budget_expense
class Budget_expense(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50, null=False)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modified_utc = models.DateField(auto_now=True, null=False)
    account = models.ForeignKey(Budget_account, on_delete=models.DO_NOTHING, default='')
    expenseType = models.ForeignKey(Expense_type, on_delete=models.DO_NOTHING, default='')
    month = models.IntegerField(choices=Month.choices, null=False)
    expense = models.DecimalField(max_digits=12, decimal_places=2, null=False)

# budget_income
class Budget_income(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50, null=False)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modified_utc = models.DateField(auto_now=True, null=False)
    account = models.ForeignKey(Budget_account, on_delete=models.DO_NOTHING, default='')
    incomeType = models.ForeignKey(Expense_type, on_delete=models.DO_NOTHING, default='')
    month = models.IntegerField(choices=Month.choices, null=False)
    income = models.DecimalField(max_digits=12, decimal_places=2, null=False)

# budget_config
class Budget_config(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50, null=False)
    created_utc = models.DateField(auto_now_add=True, null=False)
    modified_utc = models.DateField(auto_now=True, null=False)
    budget_limit = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    account = models.ForeignKey(Budget_account, on_delete=models.DO_NOTHING, default='')
    month = models.IntegerField(choices=Month.choices, null=False)

# calendar_event
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200, default='SOME STRING')
    description = models.TextField(null=True)
    start_time = models.DateTimeField(default=datetime.now, blank=True)
    end_time = models.DateTimeField(default=datetime.now, blank=True)

    @property
    def get_html_url(self):
        url = reverse('life:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'