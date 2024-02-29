from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.db import IntegrityError
from .forms import LoginForm

User = get_user_model()

# Create your views here.
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
            
    form = LoginForm()
    return render(request, 'register.html', {'form': form, 'error': error})

def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is None:
            error = "Invalid username or password."
        else:
            login(request, user)
            return redirect('booking')

    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('home')