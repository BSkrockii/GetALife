from django.urls import path
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('signOut/', views.signOut, name='signOut'),
    path('calendarFt/', views.CalendarView.as_view(), name='calendarFt'),
    path('event/', views.event, name='event'),
    path('event/edit/', views.event, name='event_edit'),
]

#urlpatterns += staticfiles_urlpatterns()