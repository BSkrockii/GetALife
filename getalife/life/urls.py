from django.urls import path
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from life.views import *
from django.urls import include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'BudgetAccount', views.Budget_accountViewSet, basename='Account')
router.register(r'ExpenseType', views.ExpenseTypeViewSet, basename='ExpenseType')
router.register(r'IncomeType', views.IncomeTypeViewSet, basename='IncomeType')
router.register(r'BudgetExpense', views.BudgetExpenseViewSet, basename='BudgetExpense')
router.register(r'BudgetIncome', views.BudgetIncomeViewSet, basename='BudgetIncome')
router.register(r'BudgetConfig', views.BudgetConfigViewSet, basename='BudgetConfig')

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('finance/', views.finance, name='finance'),
    path('cost/', views.cost, name='cost'),
    path('pay/', views.pay, name='pay'),

    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('signOut/', views.signOut, name='signOut'),
    path('checkUsername/', views.checkUsername, name='checkUsername'),
    path('calendarFt/', views.calendarFt, name='calendarFt'),
  
    # Model Access
    path('api/', include(router.urls)),

    #HTTP error Handling
    path('error_400', views.error_400, name='400_Error'),
    path('error_403', views.error_403, name='403_Error'),
    path('error_404', views.error_404, name='404_Error'),
    path('error_500', views.error_500, name='500_Error'),

    path('event/', views.event, name='event'),
    path('saveEvent/', views.saveEvent, name='saveEvent'),
    path('deleteEvent/', views.deleteEvent, name='deleteEvent'),
    path('getExpenseTypes/', views.getExpenseTypes, name='getExpenseTypes'),

    path('budget/', views.budget, name='budget'),
    path('addExpense/', views.addExpense, name='addExpense'),
    path('updateExpense/', views.updateExpense, name='updateExpense')
]

#urlpatterns += staticfiles_urlpatterns()