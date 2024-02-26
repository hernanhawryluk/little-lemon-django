from django.shortcuts import render, redirect
from django.http import HttpResponse
from items.models import Item
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.db import IntegrityError


# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def menu(request):
    items = Item.objects.all()
    return render(request, 'menu.html', {'items': items })

def signup_view(request):
    error = None
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('booking')
            except IntegrityError:
                error = 'Username already exists'
            except:
                error = 'Something went wrong'
        else:
            error = 'Passwords do not match'
            
    form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form, 'error': error})

        # form = NewUserForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     login(request, user)
        #     messages.success(request, "Registration successful." )
        # messages.error(request, "Unsuccessful registration. Invalid information.")
    

def login_view(request):
    error = None
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data = request.POST)
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is None:
            error = "Invalid username or password."
        else:
            login(request, user)
            return redirect('booking')

    form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('home')