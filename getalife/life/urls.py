from django.urls import path
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('signOut/', views.signOut, name='signOut'),

    #Create
    path('Create/budget/Account/<id>', views.CreateBudget, name='budgetAccount'),
    path('Create/budget/Expense/<id>', views.CreateExpense, name='budgetExpense'),
    path('Create/budget/Income/<id>', views.CreateIncome, name='budgetIncome'),
    path('Create/budget/Config/<id>'), views.CreateConfig, name='BudgetConfig'),
    path('Create/type/Expense/<id>', views.CreateExpenseType, name='ExpenseType'),
    path('Create/type/Income/<id>', views.CreateIncomeType, name='IncomeType'),
    
    #Read
    path('Get/budget/Account/<id>/<serializeType>', views.GetBudget, name='budgetAccount'),
    path('Get/budget/Expense/<id>/<serializeType>', views.GetExpense, name='budgetExpense'),
    path('Get/budget/Income/<id>/<serializeType>', views.GetIncome, name='budgetIncome'),
    path('Get/budget/Config/<id>/<serializeType>'), views.GetConfig, name='BudgetConfig'),
    path('Get/type/Expense/<id>/<serializeType>', views.GetExpenseType, name='ExpenseType'),
    path('Get/type/Income/<id>/<serializeType>', views.GetIncomeType, name='IncomeType'),

    #Update
    path('Put/budget/Account/<id>', views.PutBudget, name='budgetAccount'),
    path('Put/budget/Expense/<id>', views.PutExpense, name='budgetExpense'),
    path('Put/budget/Income/<id>', views.PutIncome, name='budgetIncome'),
    path('Put/budget/Config/<id>'), views.PutConfig, name='BudgetConfig'),
    path('Put/type/Expense/<id>', views.PutExpenseType, name='ExpenseType'),
    path('Put/type/Income/<id>', views.PutIncomeType, name='IncomeType'),

    #Delete
    path('Delete/budget/Account/<id>', views.DeleteBudget, name='budgetAccount'),
    path('Delete/budget/Expense/<id>', views.DeleteExpense, name='budgetExpense'),
    path('Delete/budget/Income/<id>', views.DeleteIncome, name='budgetIncome'),
    path('Delete/budget/Config/<id>'), views.DeleteConfig, name='BudgetConfig'),
    path('Delete/type/Expense/<id>', views.DeleteExpenseType, name='ExpenseType'),
    path('Delete/type/Income/<id>', views.DeleteIncomeType, name='IncomeType'),
]

#urlpatterns += staticfiles_urlpatterns()