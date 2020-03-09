from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User, auth
from datetime import datetime, timedelta, date
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm

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