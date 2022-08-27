from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import AddLibrarianForm
from models.models import Librarian
from models.models import Member
from accounts.models import PendingMemberAccounts
# Create your views here.

UserModel = get_user_model()

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            return render(request, 'admin/dashboard.html')
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class AccountManagement(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            return render(request, 'admin/accountManager.html')
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class LibrarianAccountManagement(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            return render(request, 'admin/librarian/LibrarianManager.html')

        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class AddLibrarian(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            addLibrarianForm = AddLibrarianForm()
            context = {}
            context['form'] = addLibrarianForm
            return render(request, 'admin/librarian/addLibrarian.html', context)

        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request):
        if request.user.is_admin:
            addLibrarianForm = AddLibrarianForm(request.POST)

            if addLibrarianForm.is_valid():
                if(not addLibrarianForm.cleaned_data['password1'] == addLibrarianForm.cleaned_data['password2']):
                    messages.error(request, 'Passwords do not match, please try again')
                    return redirect(reverse('adminLibAccAdd'))
                email = addLibrarianForm.cleaned_data['email']
                pwd = addLibrarianForm.cleaned_data['password1']
                name = addLibrarianForm.cleaned_data['name']
                user = UserModel.objects.create_librarian(email=email, password=pwd)
                Librarian.objects.create(name=name, userObj=user)
                return redirect(reverse('adminLibAccManage'))
        
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class DeleteLibrarian(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            libAccList = Librarian.objects.all()
            context = {}
            context['libAccList'] = libAccList
            return render(request, 'admin/librarian/delLibrarian.html', context)
            
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class DeleteAccount(LoginRequiredMixin, View):
    def get(self, request, id):
        if request.user.is_admin:
            userObj = UserModel.objects.get(id=id)
            context = {}
            context['user'] = userObj
            librarianObj = None
            memberObj = None
            if (Librarian.objects.filter(userObj=userObj).exists()):
                librarianObj = Librarian.objects.get(userObj=userObj)

            elif(Member.objects.filter(userObj=userObj).exists()):
                memberObj = Member.objects.get(userObj=userObj)
            else:
                messages.error(request, 'Such a user does not exist')
                return redirect(reverse('adminAccManage'))

            context['lib'] = librarianObj
            context['member'] = memberObj
            return render(request, 'admin/delAccount.html', context)

        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request, id):
        if request.user.is_admin:
            userObj = UserModel.objects.get(id=id)
            if (Librarian.objects.filter(userObj=userObj).exists()):
                Librarian.objects.get(userObj=userObj).delete()
                userObj.delete()
                messages.info(request, 'Librarian User deleted successfully')
                return redirect(reverse('adminAccManage'))

            elif(Member.objects.filter(userObj=userObj).exists()):
                Member.objects.get(userObj=userObj).delete()
                userObj.delete()
                messages.info(request, 'Member User deleted successfully')
                return redirect(reverse('adminAccManage'))   

            else:
                messages.error(request, 'Such a user does not exist')
                return redirect(reverse('adminAccManage'))

class MemberAccountManagement(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            return render(request, 'admin/member/MemberManager.html')

        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('adminAccManage'))

class AddMember(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            memberList = PendingMemberAccounts.objects.all()
            context = {}
            context['memberList'] = memberList
            return render(request, 'admin/member/addMember.html', context)

        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request):
        if request.user.is_admin:
            email = request.POST['email']
            name = request.POST['name']
            if 'reject' in request.POST:
                PendingMemberAccounts.objects.get(email=email).delete()
            else:
                if UserModel.objects.filter(email=email).exists():
                    messages.warning(request, 'This member already has an active account')
                    PendingMemberAccounts.objects.get(email=email).delete()
                else:
                    newUser = UserModel.objects.create_user(email=email, password='123')
                    Member.objects.create(name=name, userObj=newUser)
                    PendingMemberAccounts.objects.get(email=email).delete()
                
            return redirect(reverse('adminMemberAccAdd'))
                
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class DeleteMember(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            memberAccList = Member.objects.all()
            context = {}
            context['memberAccList'] = memberAccList
            print(context)
            return render(request, 'admin/member/delMember.html', context)
            
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class BookManagement(View):
    def get(self, request):
        return render(request, 'admin/bookManager.html')

