from django import forms
from django.forms import ModelForm
from contacts.models import Contact



class ContactForm(ModelForm):

	name = forms.CharField(widget=forms.TextInput(attrs={
			'class' : 'form-control rounded border',
			'id' : 'contact_name',
			'type' : 'text',
			'placeholder' : 'Votre nom et/ou prénom ...',
		}))


	email = forms.EmailField(widget=forms.EmailInput(attrs={
			'class' : 'form-control rounded border',
			'id' : 'contact_email',
			'type' : 'email',
			'placeholder' : 'Votre adresse email ...',
		}))

	subject = forms.CharField(widget=forms.TextInput(attrs={
			'class' : 'form-control rounded border',
			'id' : 'subject',
			'type' : 'text',
			'placeholder' : 'Votre sujet ...',
		}))

	message = forms.CharField(widget=forms.Textarea(attrs={
			'class' : 'form-control rounded border md-textarea',
			'rows' : '7',
			'id' : 'message',
			'placeholder' : 'Tapez votre message ...',
			'required' : 'true',
		}))
	
	class Meta:
		model = Contact
		fields = ['name', 'email', 'subject', 'message']
