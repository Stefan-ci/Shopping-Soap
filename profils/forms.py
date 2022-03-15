from django import forms
from profils.models import Profile
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.modelfields import PhoneNumberField

class CreateUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={
            'class': 'form-control',
			'id': 'email',
			'type': 'email',
			'name': 'email',
			'placeholder': 'Email address ',
        }))
	username = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
			'id': 'username',
			'type': 'text',
			'name': 'username',
			'placeholder': "Username ",
        }))
	password1 = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
			'id': 'password1',
			'type': 'password',
			'name': 'password1',
			'placeholder': 'Password ',
        }))
	password2 = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
			'id': 'password2',
			'type': 'password',
			'name': 'password2',
			'placeholder': 'Confirm password ',
        }))

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


# Profile details forms
class EditUserForm(ModelForm):
	email = forms.EmailField(label='Email', widget=forms.EmailInput(
		attrs={
			'class': 'form-control form-control-user',
			'id': 'email',
			'type': 'email',
			'placeholder': 'Adresse mail'
		}))
	first_name = forms.CharField(label="Prénom(s)", widget=forms.TextInput(
		attrs={
			'class': 'form-control form-control-user',
			'id': 'first_name',
			'type': 'text',
			'placeholder': 'Nom'
		}))
	last_name = forms.CharField(label="Nom", widget=forms.TextInput(
		attrs={
			'class': 'form-control form-control-user',
			'id': 'last_name',
			'type': 'text',
			'placeholder': 'Prénom(s)'
		}))

	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']






class EditProfileForm(ModelForm):
	phone_number = PhoneNumberField(region='CI')
	avatar = forms.CharField(label="Avatar", widget=forms.FileInput(
		attrs={
			'class': 'form-control form-control-user',
			'id': 'avatar',
			'type': 'file',
		}))
	class Meta:
		model = Profile
		fields = ['phone_number', 'avatar']
