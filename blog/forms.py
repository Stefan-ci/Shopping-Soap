from django import forms
from blog.models import Comment



class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    website = forms.CharField(required=False)
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'content']
