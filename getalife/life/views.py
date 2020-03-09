from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def index(request):
    context = None
    return render(request, 'life/index.html', context)

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
    #return HttpResponseRedirect(
    #    reverse(NAME_OF_PROFILE_VIEW, args=[request.user.username])
    #)
    context = None
    return render(request, 'life/home.html', context)

def login(request):
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

