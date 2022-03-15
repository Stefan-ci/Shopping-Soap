from django import forms
from menus.models import Item, Category
from taggit.managers import TaggableManager
from django.shortcuts import get_object_or_404

CATEGORY_CHOICE_QUERYSET = Category.objects.filter(is_public=True)


class CreateItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'id': 'item_name',
        'class': 'form-control form-control-sm border',
        'placeholder': 'Ex: Salade aux saucisses',
    }))
    tags = TaggableManager()
    is_public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'is_public',
        'type': 'checkbox',
        'class': 'form-check-input',
        'checked': 'true'
    }))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control border',
        'rows': '4',
        'id': 'description',
        'placeholder': 'Description du menu ...',
    }))
    price = forms.IntegerField(required=True, widget=forms.TextInput(attrs={
        'id': 'price',
        'type': 'number',
        'min': '1',
        'class': 'form-control form-control-sm border',
    }))
    discount_price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'id': 'discount_price',
        'min': '1',
        'type': 'number',
        'class': 'form-control form-control-sm border',
    }))
    category = forms.ModelChoiceField(required=True, queryset=CATEGORY_CHOICE_QUERYSET,
        to_field_name='name',
        widget=forms.TextInput(attrs={
            'id': 'name',
            'class': 'form-control form-control-sm border',
        }))
    picture = forms.ImageField(required=True)
    picture_2 = forms.ImageField(required=False)
    picture_3 = forms.ImageField(required=False)


    class Meta:
        model = Item
        fields = ['name', 'description', 'picture', 'tags', 'price', 'discount_price', 'category',
            'is_available', 'is_public', 'picture_2', 'picture_3']










class ItemUpdateForm(forms.ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'type': 'text',
        'id': 'item_name',
        'class': 'form-control form-control-sm border',
        'placeholder': 'Ex: Salade aux saucisses',
    }))
    tags = TaggableManager()
    is_public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'is_public',
        'type': 'checkbox',
        'class': 'form-check-input',
        'checked': 'true'
    }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control border',
        'rows': '4',
        'id': 'description',
        'placeholder': 'Description du menu ...',
    }))
    price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'id': 'price',
        'type': 'number',
        'min': '1',
        'class': 'form-control form-control-sm border',
    }))
    discount_price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'id': 'discount_price',
        'min': '1',
        'type': 'number',
        'class': 'form-control form-control-sm border',
    }))
    category = forms.ModelChoiceField(required=False, queryset=CATEGORY_CHOICE_QUERYSET,
        to_field_name='name',
        widget=forms.TextInput(attrs={
            'id': 'name',
            'class': 'form-control form-control-sm border',
        }))
    picture = forms.ImageField(required=False)
    picture_2 = forms.ImageField(required=False)
    picture_3 = forms.ImageField(required=False)


    class Meta:
        model = Item
        fields = ['name', 'description', 'picture', 'tags', 'price', 'discount_price', 'category',
            'is_available', 'is_public', 'picture_2', 'picture_3']

