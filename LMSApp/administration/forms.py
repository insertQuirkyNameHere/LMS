from datetime import date
from django import forms
from models.models import Book, Author

class DateInput(forms.DateInput):
    input_type =  date

class AddLibrarianForm(forms.Form):
    name = forms.CharField(max_length=50, 
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'aria-label':'name'}))

    email = forms.EmailField(max_length=120, 
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'aria-label':'email'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'aria-label':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'aria-label':'confirm password'}))


class AddBookForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Book Title', 'aria-label':'book title'}))
    authors = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Author', 'aria-label':'book author', 'list':'authorsList', 'id':'authors'}))
    genre = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Book Genre', 'aria-label':'book genre', 'list':'genreList', 'id':'genre'}))

class EditBookForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Book Title', 'aria-label':'book title'}))
    authors = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Author', 'aria-label':'book author', 'list':'authorsList', 'id':'authors'}))
    genre = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Book Genre', 'aria-label':'book genre', 'list':'genreList', 'id':'genre'}))

class AddCopiesForm(forms.Form):
    numOfCopies = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Enter Number of Copies', 'aria-label':'Enter Number of Copies'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder':'Copy Price', 'aria-label':'Copy Price'}))

class EditCopiesForm(forms.Form):
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder':'Copy Price', 'aria-label':'Copy Price'}))
    isIssued = forms.BooleanField(label='Copy Issued?')
    issuedDate = forms.DateField(widget=DateInput(attrs={'type':'date', 'disabled':'true'}), label='Issue Date', required=False)
    returnDate = forms.DateField(widget=DateInput(attrs={'type':'date', 'disabled':'true'}), label='Return Date', required=False)
