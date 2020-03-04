from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView, View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.forms.models import modelform_factory
from .models import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        redirect('/home')
    return render(request, 'life/index.html')

def home(request):
    if request.user.is_authenticated:
        context = None
        return render(request, 'life/home.html', context)
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

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('register')
    else:
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