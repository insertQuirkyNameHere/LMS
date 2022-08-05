from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .models import PendingMemberAccounts
from .forms import LoginForm, MemberRegisterForm
# Create your views here.

class HomePage(View):
    def get(self, request):
        return render(request, 'accounts/home.html')

class LoginView(View):
    def get(self, request):
        loginForm = LoginForm()
        context ={}
        context['form'] = loginForm
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            email = loginForm.cleaned_data['email']
            password = loginForm.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None: 
                login(request, user)
                print(user)
                if user.is_admin is True:
                    return(redirect(reverse('adminDash')))

            else:
                messages.error(request, 'Invalid Credentials')
                return (redirect(reverse('login')))

class MemberRegisterView(View):
    def get(self, request):
        registerForm = MemberRegisterForm()
        context = {}
        context['form'] = registerForm
        return render(request, 'accounts/register/member.html', context)

    def post(self, request):
        registerForm = MemberRegisterForm(request.POST)

        if registerForm.is_valid():
            registerForm.save()
        else:
            messages.info(request, 'Your request has already been logged. It will be processed soon')

        
        return (redirect(reverse('home')))

class UserScramble(View):
    def get(self, request):
        if request.user.is_admin:
            return redirect(reverse('adminDash'))
        elif request.user.is_lib:
            return redirect(reverse('libDash'))
        elif request.user.is_member:
            return redirect(reverse('memberDash'))




