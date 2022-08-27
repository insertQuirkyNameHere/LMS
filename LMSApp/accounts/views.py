from importlib.resources import contents
from multiprocessing import context
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .models import PendingMemberAccounts
from .forms import LoginForm, MemberRegisterForm, ResetPasswordForm
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
                return redirect(reverse('userScramble'))

            else:
                print('Invalid credos')
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

class PasswordReset(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = ResetPasswordForm({'email':user.email})
        context = {}
        context['form'] = form
        return render(request, 'accounts/passwordReset.html', context)

    def post(self, request):
        passwordResetForm = ResetPasswordForm(request.POST)

        if passwordResetForm.is_valid():
            USERMODEL = get_user_model()
            email = passwordResetForm.cleaned_data['email']
            userExists = USERMODEL.objects.filter(email=email).exists()
            if (not userExists):
                messages.error(request, 'User with such an email address does not exist')
                return redirect('home')

            user = authenticate(email=email, password=passwordResetForm.cleaned_data['oldPassword'])
            if user:
                if passwordResetForm.cleaned_data['newPassword'] == passwordResetForm.cleaned_data['confirmPassword']:
                    user.set_password(passwordResetForm.cleaned_data['newPassword'])
                    user.save()
                    print('Password Change')
                    messages.success(request, 'Password changed successfully')
                    return redirect(reverse('home'))
                else:
                    messages.warning(request, 'New passwords do not match')
                    return redirect(reverse('passwordReset'))
            else:
                messages.error(request, 'Incorrect Password or email')
                return redirect(reverse('passwordReset'))
            
class UserScramble(View):
    def get(self, request):
        if request.user.is_admin:
            return redirect(reverse('adminDash'))
        elif request.user.is_lib:
            return redirect(reverse('libDash'))
        elif request.user.is_member:
            return redirect(reverse('memberDash'))




