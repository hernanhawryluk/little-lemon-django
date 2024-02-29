from django import forms

class LoginForm(forms.Form):
    # username = forms.CharField()
    email = forms.EmailField(label='Email', max_length = 120, required = True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)