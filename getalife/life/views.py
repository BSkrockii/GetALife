import os
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, auth
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.forms.models import modelform_factory
from datetime import datetime, timedelta, date
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from .utils import Calendar
from .forms import EventForm
from .models import *

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
        return render(request, 'life/home.html', context)
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
    context = None
    return render(request, 'life/event.html', context)

class CalendarView(generic.ListView):
    model = Event
    template_name = 'life/calendarFt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        calendar = Calendar(d.year, d.month)
        html_cal = calendar.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendarFt'))
    return render(request, 'life/event.html', {'forms': form})
