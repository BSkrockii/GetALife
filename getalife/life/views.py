import os
import json
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, auth
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.core import serializers
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
from rest_framework.response import Response
from .serializers import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        redirect('/dashboard')
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
        return redirect('/home')
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
        return redirect('/login')
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
    return render(request, 'life/error_400.html', context)

def error_403(request, exception):
    context = None
    context = {"project_name":settings.PROJECT_NAME}
    return render(request, 'life/error_403.html', context)

def error_404(request, exception):
    context = None
    context = {"project_name":settings.PROJECT_NAME}
    return render(request,'life/error_404.html', context)

def error_500(request):
    context = None
    context = {"project_name":settings.PROJECT_NAME}
    return render(request,'life/error_500.html', context)

def calendarFt(request):
    context = None
    return render(request, 'life/calendarFt.html', context)

def event(request):
    all_events = serializers.serialize('json', Events.objects.filter(user_id=request.user))
    return JsonResponse(all_events, safe=False)

@csrf_exempt
def saveEvent(request):
    if request.user.is_authenticated:
        formatedDate = datetime.strptime(request.POST['date'], '%m/%d/%Y')
        event = Events(event_name=request.POST['event'],
                start_date=formatedDate, 
                end_date=formatedDate, 
                event_type='expense',
                amount=request.POST['amount'],
                user_id=request.user)
        event.save()

    return JsonResponse({'id':event.pk}, status=200)
    
@csrf_exempt
def deleteEvent(request):
    event = Events.objects.filter(user_id=request.user, event_id=request.POST['id'])
    event.delete()
    return JsonResponse({}, status=200)

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
            accts = Budget_account.objects.filter(users = request.user)
            querySet = Budget_expense.objects.select_related('account')

            serializer = Budget_expenseSerializer(querySet, many=True, allow_null=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            accts = Budget_account.objects.filter(users = request.user)
            querySet = Budget_expense.objects.select_related('account')
            querySet.filter(id = pk)

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
            accts = Budget_account.objects.filter(users = request.user)
            querySet = Budget_income.objects.select_related('account')

            serializer = Budget_incomeSerializer(querySet, many=True, allow_null=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            accts = Budget_account.objects.filter(users = request.user)
            querySet = Budget_income.objects.select_related('account')
            querySet.filter(id = pk)

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
            accts = Budget_account.objects.filter(users = request.user)
            querySet = Budget_config.objects.select_related('account')

            serializer = Budget_configSerializer(querySet, many=True, allow_null=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            accts = Budget_account.objects.filter(users = request.user)
            querySet = Budget_config.objects.select_related('account')
            querySet.filter(id = pk)

            serializer = Budget_configSerializer(querySet, many=True, allow_null=True)

            return Response(serializer.data)

# # budget_config
# class Budget_configSerializer(serializers.HyperlinkedModelSerializer):
#     model = Budget_config
#     fields = ['id', 'name', 'description', 'budget_limit', 'account', 'month']
