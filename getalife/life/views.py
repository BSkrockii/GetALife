import os
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
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        redirect('/home')
    return render(request, 'life/index.html')

def home(request):
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
            return redirect('/home')
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
    context = {}
    context = {"project_name":settings.PROJECT_NAME}
    return render(request, 'life/error_400.html', context)

def error_400_demo(request):
    context = {}
    context = {"project_name":settings.PROJECT_NAME}
    return render(request, 'life/error_400.html', context)

def error_403(request, exception):
    context = {}
    context = {"project_name":settings.PROJECT_NAME}
    return render(request, 'life/error_403.html', context)

def error_403_demo(request):
    context = {}
    context = {"project_name":settings.PROJECT_NAME}
    return render(request, 'life/error_403.html', context)

def error_404(request, exception):
    context = {}
    context = {"project_name":settings.PROJECT_NAME}
    return render(request,'life/error_404.html', context)

def error_404_demo(request):
    context = {}
    context = {"project_name":settings.PROJECT_NAME}
    return render(request,'life/error_404.html', context)

def error_500(request):
    context = {}
    context = {"project_name":settings.PROJECT_NAME}
    return render(request,'life/error_500.html', context)

def error_500_demo(request):
    context = {}
    context = {"project_name":settings.PROJECT_NAME}
    return render(request,'life/error_500.html', context)

# Restful api
class BudgetAccount(View):
    def get(self, request):
        account = Budget_account.objects.filter(id=request.GET['id'])
        ser = serializers.serialize('json', account)
        return JsonResponse(ser, status = 200, safe = False)

    # create and update
    def put(self, request):
        modelForm = modelform_factory(Budget_account)
        form = modelform(request.PUT)
        if form.is_Valid():
            form.save()
            return JsonResponse({}, status = 200, safe = False)
        return JsonResponse({form})
        
    def delete(self, request):
        Budget_account.objects.get(id = request.DELETE('id')).delete()
        return JsonResponse({}, status=200)

class BudgetConfig(View):
    def get(self, request):
        account = Budget_config.objects.get(id=request.GET['id'])
        return JsonResponse(account, status = 200, safe = False)

    # create and update
    def put(self, request):
        modelForm = modelform_factory(Budget_config)
        form = modelform(request.PUT)
        if form.is_Valid():
            form.save()
            return JsonResponse({}, status = 200, safe = False)
        return JsonResponse({form})
        
    def delete(self, request):
        Budget_config.objects.get(id = request.DELETE('id')).delete()
        return JsonResponse({}, status=200)

class BudgetIncome(View):
    def get(self, request):
        account = Budget_Income.objects.get(id=request.GET['id'])
        ser = serializers.serialize('json', account)
        return JsonResponse(ser, status = 200, safe = False)

    # create and update
    def put(self, request):
        modelForm = modelform_factory(Budget_Income)
        form = modelform(request.PUT)
        if form.is_Valid():
            form.save()
            return JsonResponse({}, status = 200, safe = False)
        return JsonResponse({form})
        
    def delete(self, request):
        Budget_Income.objects.get(id = request.DELETE('id')).delete()
        return JsonResponse({}, status=200)

class BudgetExpense(View):
    def get(self, request):
        account = Budget_Expense.objects.get(id=request.GET['id'])
        ser = serializers.serialize('json', account)
        return JsonResponse(ser, status = 200, safe = False)

    # create and update
    def put(self, request):
        modelForm = modelform_factory(Budget_Expense)
        form = modelform(request.PUT)
        if form.is_Valid():
            form.save()
            return JsonResponse({}, status = 200, safe = False)
        return JsonResponse({form})
        
    def delete(self, request):
        Budget_Expense.objects.get(id = request.DELETE('id')).delete()
        return JsonResponse({}, status=200) 


class TypeIncome(View):
    def get(self, request):
        account = Income_Type.objects.get(id=request.GET['id'])
        ser = serializers.serialize('json', account)
        return JsonResponse(ser, status = 200, safe = False)

    # create and update
    def put(self, request):
        modelForm = modelform_factory(Income_Type)
        form = modelform(request.PUT)
        if form.is_Valid():
            form.save()
            return JsonResponse({}, status = 200, safe = False)
        return JsonResponse({form})
        
    def delete(self, request):
        Income_Type.objects.get(id = request.DELETE('id')).delete()
        return JsonResponse({}, status=200) 

class TypeExpense(View):
    def get(self, request):
        account = Expense_Type.objects.get(id=request.GET['id'])
        ser = serializers.serialize('json', account)
        return JsonResponse(ser, status = 200, safe = False)

    # create and update
    def put(self, request):
        modelForm = modelform_factory(Expense_Type)
        form = modelform(request.PUT)
        if form.is_Valid():
            form.save()
            return JsonResponse({}, status = 200, safe = False)
        return JsonResponse({form})
        
    def delete(self, request):
        Expense_Type.objects.get(id = request.DELETE('id')).delete()
        return JsonResponse({}, status=200) 

        
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