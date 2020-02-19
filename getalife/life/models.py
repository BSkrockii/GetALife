from django.conf import settings
from django.db import models

# Create your models here.



# financial_management_budget
class budgetAccount(models.Model):
    # Many-Many relationship to user model
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    created = models.DateField(auto_now=False, auto_now_add=True)
    modefied = models.DateField(auto_now=True, auto_now_add=False)


# financial_management_budget_expense
# id UUID
# budget_id UUID
# name nvarchar(50)
# expense_type: int
# description: nvarchar(150)
# month int (or 4 bits)
# created (datetime(6))
# modified(datetime(6))


# financial_management_budget_expense_type
# type int
# description nvarchar(50)
# created: datetime(6)
# modfied: datetime(6)

# financial_management_budget_income
# id UUID
# budget_id UUID
# name nvarchar(50)
# expense_type: int
# description: nvarchar(150)
# month int (or 4 bits)
# created (datetime(6))
# modified(datetime(6))

# financial_management_budget_income_type
# type int
# description nvarchar(50)
# created: datetime(6)
# modfied: datetime(6)

# financial_management_budget_config