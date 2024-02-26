from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required = True)
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	# def save(self, commit=True):
	# 	user = super(CustomUserCreationForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user
	
class CustomAuthenticationForm(AuthenticationForm):
	pass
	# username = forms.EmailField(
    #     max_length=254,
    #     widget=forms.EmailInput(attrs={'autofocus': True}),
    # )