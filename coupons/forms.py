from django import forms
from coupons.models import Coupon

class CouponForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Entrez votre code coupon',
        }))
    class Meta:
        model = Coupon
        fields = ['code']
