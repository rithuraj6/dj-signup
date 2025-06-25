from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re




@never_cache
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'GET':
        return render(request, "login.html")

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
 

      


@never_cache
def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="GET":
         return render(request, "Signup.html")
     
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        
        if User.objects.filter(username=username).exists():
            messages.info(request, "User already exists. Please log in.")
            return redirect('login')

        
        if not username or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
            return redirect('signup')

        
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request, 'Enter a valid email address.')
            return redirect('signup')
        

       

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signup')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, 'Signup successful! Please login.')
        return redirect('login')

   



@never_cache
@login_required(login_url='login')
def home(request):
    return render(request, "home.html")

@never_cache
@login_required(login_url='login')
def about(request):
    return render(request, "about.html")

@never_cache
@login_required(login_url='login')
def contact(request):
    return render(request, "contact.html")

def logout_user(request):
    logout(request)
    request.session.flush()
    messages.success(request, "You have successfully logged out.")
    return redirect('signup')


