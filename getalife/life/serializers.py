from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class Budget_AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget_account
        fields = ['id', 'name', 'description']
        
# budget_expense_type
class Expense_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense_type
        fields = ['id', 'name', 'description']

# budget_income_type
class Income_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income_type
        fields = ['id', 'name', 'description']

# budget_expense
class Budget_expenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget_expense
        fields = ['id', 'name', 'description', 'account', 'expenseType', 'month', 'expense']

# budget_income
class Budget_incomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget_income
        fields = ['id', 'name', 'description', 'account', 'incomeType', 'month', 'income']

# budget_config
class Budget_configSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget_config
        fields = ['id', 'name', 'description', 'budget_limit', 'account', 'month']