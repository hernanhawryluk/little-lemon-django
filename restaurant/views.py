from django.shortcuts import render, redirect
from items.models import Item
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomAuthenticationForm


# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def menu(request):
    items = Item.objects.all()
    return render(request, 'menu.html', {'items': items })

def booking(request):
    return render(request, 'booking.html', {'range': range(2, 13)})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('booking')
            else:
                messages.error(request, "Invalid username or password.")
                error = "Invalid username or password."

        else:
            messages.error(request, "Invalid username or password.")
            error = "Invalid username or password."
    form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form, 'error': error})
