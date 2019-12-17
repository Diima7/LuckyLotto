from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LogoutView

app_name = 'webs'       # Die datei ist damit django weiß was wozu gehört
urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),    #z.b die seite /login/ gehört zu der def login_view() in der datei views.py
    path('register/', views.register_view, name='register'),
    path('about/', views.about_view, name='about'),
    path('lotto/', views.lotto_view, name='lotto'),
    path('logout/', views.logout_view,name='logout'),
    
]

urlpatterns += staticfiles_urlpatterns()
