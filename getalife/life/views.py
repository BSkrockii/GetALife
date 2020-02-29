from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, auth

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
        passrepeat = request.POST['passrepeat']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('/register')

        if email == '':
            messages.error(request, 'Email is required')
            return redirect('/register')
        
        if len(password) <= 6:
            messages.error(request, 'Password must be 7 or more characters')
            return redirect('/register')

        if password != passrepeat:
            messages.error(request, 'Passwords do not match')
            return redirect('/register')

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
