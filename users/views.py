from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.db import IntegrityError
from .forms import LoginForm, RegisterForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,  TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token

User = get_user_model()

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
            
    form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'error': error})


def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        user = authenticate(email = request.POST['email'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('booking')
        else:
            error = "Invalid username or password."
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


@api_view(['POST'])
def login_api(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_404_NOT_FOUND)
    
    user = get_object_or_404(User, email = email)
    if not user.check_password(password):
        return  Response({'detail': 'Not found'}, status = status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user = user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data}, status = status.HTTP_200_OK)


@api_view(['POST'])
def signup_api(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username = request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user = user)
        return Response({'token': token.key, 'user': serializer.data}, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token_api(request):
    return Response('passed for {}'.format(request.user.email), status = status.HTTP_200_OK)