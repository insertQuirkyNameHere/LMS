from django.forms import Form, ModelForm
from django import forms

from .models import PendingMemberAccounts

class LoginForm(Form):
    email = forms.EmailField(max_length=120, widget=forms.EmailInput(attrs={'placeholder':'email', 'aria-label':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'aria-label':'Password'}))

class MemberRegisterForm(ModelForm):
    class Meta:
        model = PendingMemberAccounts
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'Name', 'aria-label':'name'}),
            'email': forms.EmailInput(attrs={'placeholder':'email', 'aria-label':'email'}),
        }
        