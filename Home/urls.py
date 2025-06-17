from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('home/', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
   
    path('logout/', views.logout_user, name='logout'),

]
