from django import forms
from django.forms import ModelForm
from refunds.models import Refund


class RefundForm(forms.Form):
    unique_code = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'unique_code',
            'type': 'text',
            'required': 'true',
            'placeholder': 'Le code de votre commande ...',
        }))
    name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'type': 'text',
            'required': 'true',
            'placeholder': 'Votre nom ...',
        }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'type': 'email',
            'placeholder': 'Votre adresse mail valide/valable ...',
            'required': 'true',
        }))
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': '7',
            'id': 'message',
            'placeholder': 'Pourquoi voulez-vous vous faire rembourser ?',
            'required': 'true',
        }))
