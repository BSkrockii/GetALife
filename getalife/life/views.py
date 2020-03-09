from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, auth
from django.conf import settings

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
