from django import forms
from address.models import ShippingCity, ShippingCountry
from dynamic_forms import DynamicFormMixin, DynamicField
from phonenumber_field.formfields import PhoneNumberField





class CheckoutForm(DynamicFormMixin, forms.Form):
	try:
		default_country = ShippingCountry.objects.get(country="CI")
	except:
		default_country = ShippingCountry.objects.first()

	def city_choices(form):
		country = form['shipping_country'].value()
		return ShippingCity.objects.filter(country=country)
		
	def initial_city(form):
		country = form['shipping_country'].value()
		return ShippingCity.objects.filter(country=country).first()

	first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Nom ...'}))
	last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Prenom(s) ...'}))
	email_address = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email ...'}))
	shipping_country = forms.ModelChoiceField(
		queryset=ShippingCountry.objects.all(),
		initial=default_country
	)
	shipping_city = DynamicField(
		forms.ModelChoiceField,
		queryset=city_choices,
		initial=initial_city
	)
 



class OrderConfirmForm(forms.Form):
	confirm_order = forms.BooleanField(required=False)
	phone_number = PhoneNumberField(
		widget=forms.TextInput(attrs={'placeholder': '(+2250707070707)'})
	)
