from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length = 120)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length = 80)
    email = forms.EmailField(label='Email', max_length = 120)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)