from django.urls import path
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('finance/', views.finance, name='finance'),
    path('cost/', views.cost, name='cost'),
    path('pay/', views.pay, name='pay'),
]

#urlpatterns += staticfiles_urlpatterns()