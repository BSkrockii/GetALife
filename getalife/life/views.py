import os
import json
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, auth
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.core import serializers as ser
from django.http import HttpResponse, JsonResponse
from django.forms.models import modelform_factory, model_to_dict
from datetime import datetime, timedelta, date
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from django.db.models import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'life/index.html')

def finance(request):
    context = None
    return render(request, 'life/finance.html', context)

def cost(request):
    context = None
    return render(request, 'life/cost.html', context)

def pay(request):
    context = None
    return render(request, 'life/pay.html', context)

def home(request):
    if request.user.is_authenticated:
        context = None
        return render(request, 'life/dashboard.html', context)
    return redirect('/login')

def dashboard(request):
    if request.user.is_authenticated:
        context = None
        return render(request, 'life/dashboard.html', context)
    return redirect('/login')
    
def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/dashboard')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'life/login.html')

def checkUsername(request):
    username = request.GET['username']
    if User.objects.filter(username=username).exists():
        return JsonResponse({'username':True})
    return JsonResponse({'username':False})


def register(request):
    print(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        passrepeat = request.POST['passrepeat']
        email = request.POST['email']

        context = {
            "username": username,
            "email" : email
        }

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'life/register.html', context)

        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters')
            return render(request, 'life/register.html', context)

        if email == '':
            messages.error(request, 'Email is required')
            return render(request, 'life/register.html', context)
        
        if len(password) <= 6:
            messages.error(request, 'Password must be 7 or more characters')
            return render(request,'life/register.html', context)

        if password != passrepeat:
            messages.error(request, 'Passwords do not match')
            return render(request,'life/register.html', context)


        user = User.objects.create_user(username=username, password=password,email=email)
        user.save()
        request.user = user

        # budgetAccount
        date = datetime.now()
        acct = Budget_account.objects.create(name = date.year, description = date.strftime('%B'), month = date.month)

        # add to user
        acct.users.add(user)

        # Add Config
        conf = Budget_config.objects.create(name = acct.name, description = 'config', budget_limit = 10000, month = date.month, account_id = acct.id)

        # add expense
        expense = Budget_expense.objects.create(name = 'expense ' + date.strftime('%B'), description = date.year, month = date.month, account_id = acct.id, expense = 10000, expenseType_id = 1)

        # add income
        income = Budget_income.objects.create(name = 'income ' + date.strftime('%B'), description = date.year, month = date.month, account_id = acct.id, income = 10000, incomeType_id = 1)

        acct.save()
        conf.save()
        expense.save()
        income.save()

        return redirect('/dashboard')
    return render(request, 'life/register.html')

def faq(request):
    context = None
    return render(request, 'life/faq.html', context)

def about(request):
    context = None
    return render(request, 'life/about.html', context)

def signOut(request):
    auth.logout(request)
    return redirect('/login')

# Http Error Handling
def error_400(request, exception):
    context = None
    context = {"project_name":settings.PROJECT_NAME}
    return render(request, 'life/error_400.html', context, status=400)

def error_403(request, exception):
    context = None
    context = {"project_name":settings.PROJECT_NAME}
    return render(request, 'life/error_403.html', context, status=403)

def error_404(request, exception):
    context = None
    context = {"project_name":settings.PROJECT_NAME}
    return render(request,'life/error_404.html', context, status=404)

def error_500(request):
    context = None
    context = {"project_name":settings.PROJECT_NAME}
    return render(request,'life/error_500.html', context, status=500)

def calendarFt(request):
    if request.user.is_authenticated:
        context = None
        return render(request, 'life/calendarFt.html', context)
    else:
        return redirect('login')

def event(request):
    if request.user.is_authenticated:
        all_events = ser.serialize('json', Events.objects.filter(user_id=request.user))
        return JsonResponse(all_events, safe=False)
    else:
        return JsonResponse({}, status=403)

@csrf_exempt
def saveEvent(request):
    if request.user.is_authenticated:
        formatedDate = datetime.strptime(request.POST['date'], '%m/%d/%Y')
        event = Events(event_name=request.POST['event'],
                start_date=formatedDate, 
                end_date=formatedDate, 
                event_type=request.POST['expenseType'],
                amount=request.POST['amount'],
                user_id=request.user)
        event.save()
    else:
        return JsonResponse({}, status=403)
    return JsonResponse({'id':event.pk}, status=200)
    
@csrf_exempt
def deleteEvent(request):
    event = Events.objects.filter(user_id=request.user, event_id=request.POST['id'])
    event.delete()
    return JsonResponse({}, status=200)

@csrf_exempt
def getExpenseTypes(request):
    date = datetime.strptime(request.GET['date'], '%m/%d/%Y')
    print(date.month)
    expenseType = list(Budget_expense.objects.values('name').distinct().filter(account__users=request.user, month=date.month))
    print(expenseType)
    return JsonResponse(json.dumps(expenseType), safe=False, status=200)

# Api
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class Budget_accountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view or edit account
    Only see user's associated accounts
    """

    serializer_class = Budget_AccountSerializer
    queryset = Budget_account.objects.all()

    def list(self, request):
        if request.user.is_authenticated:
            querySet = Budget_account.objects.filter(users = request.user)
            serializer = Budget_AccountSerializer(querySet, many=True, allow_null=True)
            
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            querySet = Budget_account.objects.filter(users = request.user, id = pk)
            serializer = Budget_AccountSerializer(querySet, many=True, allow_null=True)

            return Response(serializer.data)

    def create(self, request):
        if request.user.is_authenticated:

            datas = request.data
            account = Budget_account.objects.create(name = request.data['name'], description = request.data['description'])
            
            account.users.add(request.user)
            account.save()
            
            serializer = Budget_AccountSerializer(account, many=False, allow_null=True)

            return Response(serializer.data, status=200)

    @action(detail=True, methods=['get'], url_path='users')
    def userList(self,request,pk):
        if request.user.is_authenticated:
            budget = Budget_account.objects.get(users = request.user, id = pk)
            users = budget.users.all()
            
            serializer = UserSerializer(users, many=True, allow_null=True)
            return Response(serializer.data)


    @action(detail=True, methods=['get', 'post', 'delete'], url_path='users/(?P<userId>[^/.]+)')
    def addUser(self, request, pk, userId):
        """
        Adds a user authZ to budgetAccount
        """
        if request.user.is_authenticated:
            if request.method == 'GET':
                budget = Budget_account.objects.get(users = request.user, id = pk)
                user = budget.users.filter(id = userId)
                serializer = UserSerializer(user, many=True, allow_null=True)

                return Response(serializer.data)

            if request.method == 'POST':
                check = request.data
                budget = Budget_account.objects.get(users = request.user, id = pk)
                
                user = User.objects.filter(id = userId)
                if len(user) == 0:
                    return Response(['user not found'], status=404)
                
                budget.users.add(user[0])
                budget.save()
                return Response({}, status=200)
            
            if request.method == 'DELETE':
                budget = Budget_account.objects.get(users = request.user, id = pk)

                user = User.objects.filter(id = userId)
                if len(user) == 0:
                    return Response(['User not found'], status=404)

                usr = user[0]
                budget.users.remove(usr)
                budget.users.save()
                budget.save()
                return Response({}, status=200)
            
        return Response(status=403)


class ExpenseTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view or edit expense type
    Only Admins can access this!  If public has access to this, then anyone can edit these records.
    """

    queryset = Expense_type.objects.all()
    serializer_class = Expense_typeSerializer
    permission_classes = [permissions.IsAdminUser]

class IncomeTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view or edit income type
    Only Admins can access this!  If public has access to this, then anyone can edit these records.
    """

    queryset = Income_type.objects.all()
    serializer_class = Income_typeSerializer
    permission_classes = [permissions.IsAdminUser]


class BudgetExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view or edit account
    Only see user's associated accounts
    """

    serializer_class = Budget_expenseSerializer
    queryset = Budget_expense.objects.all()

    def list(self, request):
        if request.user.is_authenticated:
            querySet = Budget_expense.objects.filter(account__users__id=request.user.id)

            serializer = Budget_expenseSerializer(querySet, many=True, allow_null=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            querySet = Budget_expense.objects.filter(account__users__id=request.user.id)
            querySet = querySet.filter(id = pk)


            serializer = Budget_expenseSerializer(querySet, many=True, allow_null=True)

            return Response(serializer.data)


class BudgetIncomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view or edit account
    Only see user's associated accounts
    """

    serializer_class = Budget_incomeSerializer
    queryset = Budget_income.objects.all()

    def list(self, request):
        if request.user.is_authenticated:
            querySet = Budget_income.objects.filter(account__users__id=request.user.id)

            serializer = Budget_incomeSerializer(querySet, many=True, allow_null=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            querySet = Budget_income.objects.filter(account__users__id=request.user.id)
            querySet = querySet.filter(id = pk)

            serializer = Budget_incomeSerializer(querySet, many=True, allow_null=True)

            return Response(serializer.data)


class BudgetConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow to view or edit account
    Only see user's associated accounts
    """

    serializer_class = Budget_configSerializer
    queryset = Budget_config.objects.all()

    def list(self, request):
        if request.user.is_authenticated:
            querySet = Budget_config.objects.filter(account__users__id=request.user.id)

            serializer = Budget_configSerializer(querySet, many=True, allow_null=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            querySet = Budget_config.objects.filter(account__users__id=request.user.id)
            querySet = querySet.filter(id = pk)

            serializer = Budget_configSerializer(querySet, many=True, allow_null=True)

            return Response(serializer.data)


def budget(request):
    if request.user.is_authenticated is False:
        return redirect('/')
    budgetYears = Budget_account.objects.values('name').distinct().filter(users=request.user).order_by('name')

    budgetYearData = {}
    for by in budgetYears:
        budgetYearData[by['name']] = Budget_account.objects.filter(users=request.user, name=by['name'])  


    temp = Budget_expense.objects.filter(account__users__id=request.user.id)

    Data = {}

    for by in budgetYears:
        tempMonth = {}
        for month in range(1, 13):
            tempEvent = {}
            distinctEvents = Events.objects.values('event_type').distinct().filter(user_id=request.user, start_date__month=str(month), start_date__year=by['name'])
            for event in distinctEvents:
                tempEvent[event['event_type']] = Events.objects.values('amount').filter(user_id=request.user, event_type=event['event_type'], start_date__month=str(month), start_date__year=by['name']).aggregate(amount=Sum('amount'))
                
            tempMonth[month] = tempEvent
        Data[by['name']] = tempMonth


    budgetData = Budget_account.objects.filter(users=request.user)
    return render(request,'life/budget.html', {"budgetData":budgetData, 
            "budgetYears": budgetYears, 
            "budgetYearData":budgetYearData, 
            "budgetMonthData":temp,
            "eventData": Data })

@csrf_exempt
def addExpense(request):
    newExpense = request.POST['newExpense']
    newPlanned = request.POST['newPlanned']
    month = request.POST['month'].lower()
    year = request.POST['year']
    
    monthNum = 0
    
    if month == 'january':
        monthNum = 1
    elif month == 'febuary':
        monthNum = 2
    elif month == 'march':
        monthNum = 3
    elif month == 'april':
        monthNum = 4   
    elif month == 'may':
        monthNum = 5    
    elif month == 'june':
        monthNum = 6    
    elif month == 'july':
        monthNum = 7
    elif month == 'august':
        monthNum = 8
    elif month == 'september':
        monthNum = 9
    elif month == 'october':
        monthNum = 10
    elif month == 'november':
        monthNum = 11
    else:
        monthNum = 12

    account_id = Budget_account.objects.filter(description=month, name=year, users__id=request.user.id)
    expenseType = Expense_type.objects.filter(id=1)

    expense = Budget_expense(
           name = newExpense,
           description = year,
           month = monthNum,
           expense = newPlanned, 
           account = account_id[0],
           expenseType = expenseType[0])
    expense.save()
    
    return JsonResponse({}, status=200)

@csrf_exempt
def updateExpense(request):
    updatedExpense = request.POST['budgetName']
    updatedPlanned = request.POST['planned']
    month = request.POST['month'].lower()
    year = request.POST['year']
    temp = request.POST['oldValue']
    monthNum = 0
    
    if month == 'january':
        monthNum = 1
    elif month == 'febuary':
        monthNum = 2
    elif month == 'march':
        monthNum = 3
    elif month == 'april':
        monthNum = 4   
    elif month == 'may':
        monthNum = 5    
    elif month == 'june':
        monthNum = 6    
    elif month == 'july':
        monthNum = 7
    elif month == 'august':
        monthNum = 8
    elif month == 'september':
        monthNum = 9
    elif month == 'october':
        monthNum = 10
    elif month == 'november':
        monthNum = 11
    else:
        monthNum = 12

    temp2 = Budget_expense.objects.filter(month=monthNum, description=year, name=temp, account__users=request.user).update(name=updatedExpense, expense=updatedPlanned)

    other = Events.objects.filter(start_date__month=monthNum, start_date__year=str(year), user_id=request.user, event_type=temp).update(event_type=updatedExpense)

    #temp.save()
    return JsonResponse({}, status=200)

@csrf_exempt
def getAvailableMonths(request):
    year = request.GET['year']
    months = list(Budget_account.objects.values('month').filter(name=year, users__id=request.user.id))
    return JsonResponse(json.dumps(months), safe=False, status=200)

@csrf_exempt
def addBudget(request):
    year = request.POST['year']
    month = request.POST['month'].lower()

    monthNum = 0
    
    if month == 'january':
        monthNum = 1
    elif month == 'febuary':
        monthNum = 2
    elif month == 'march':
        monthNum = 3
    elif month == 'april':
        monthNum = 4   
    elif month == 'may':
        monthNum = 5    
    elif month == 'june':
        monthNum = 6    
    elif month == 'july':
        monthNum = 7
    elif month == 'august':
        monthNum = 8
    elif month == 'september':
        monthNum = 9
    elif month == 'october':
        monthNum = 10
    elif month == 'november':
        monthNum = 11
    else:
        monthNum = 12

    budget = Budget_account.objects.create(name = year, description = month, month = monthNum)
    budget.save()
    budget.users.add(request.user)
    return JsonResponse({}, status=200)
