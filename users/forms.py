from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30,widget=forms.PasswordInput)

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ["username","email","password1","password2"]

class ProfileRegisterForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ["image"]

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username",]

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ["image",]

