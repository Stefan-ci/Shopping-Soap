from django import forms
from coupons.models import Coupon

class CouponForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Code de promotion',
            'aria-label': 'Recipient\'s username',
            'aria-describedby': 'basic-addon2',
            'name' : 'code',
        }))
    class Meta:
        model = Coupon
        fields = ['code']
