from django.urls import path
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from life.views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('signOut/', views.signOut, name='signOut'),
    path('checkUsername/', views.checkUsername, name='checkUsername'),
    path('calendarFt/', views.calendarFt, name='calendarFt'),
  
    # Model Access
    path('api/budget/Account/', BudgetAccount.as_view()),
    path('api/budget/Config/', BudgetConfig.as_view()),
    path('api/budget/Income/', BudgetIncome.as_view()),
    path('api/budget/Expense/', BudgetExpense.as_view()),
    path('api/type/Expense/', TypeExpense.as_view()),
    path('api/type/Income/', TypeIncome.as_view()),
  
    #HTTP error Handling
    path('error_400_demo/', views.error_400_demo, name='400_Error'),
    path('error_403_demo/', views.error_403_demo, name='403_Error'),
    path('error_404_demo/', views.error_404_demo, name='404_Error'),
    path('error_500_demo/', views.error_500_demo, name='500_Error'),

    path('event/', views.event, name='event'),
    path('saveEvent/', views.saveEvent, name='saveEvent'),
    path('deleteEvent/', views.deleteEvent, name='deleteEvent'),
]

#urlpatterns += staticfiles_urlpatterns()