from django import forms

class AddLibrarianForm(forms.Form):
    name = forms.CharField(max_length=50, 
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'aria-label':'name'}))

    email = forms.EmailField(max_length=120, 
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'aria-label':'email'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'aria-label':'password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'aria-label':'confirm password'}))
