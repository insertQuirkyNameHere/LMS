import datetime as DT
from multiprocessing import context

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View

from models.models import *  

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

UserModel = get_user_model()
class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'member/dashboard.html')

class BookList(LoginRequiredMixin, View):
    def get(self, request):
        bookList = Book.objects.all()
        context = {}
        context['bookList'] = bookList
        return render(request, 'member/bookList.html', context)

class BookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        issuedCopies = book.copy_set.filter(isIssued=True)
        unissuedCopies = book.copy_set.filter(isIssued=False)
        context = {}
        context['book'] = book
        context['issuedCopies'] = issuedCopies
        context['unissuedCopies'] = unissuedCopies
        return render(request, 'member/bookView.html', context)

class CopyView(LoginRequiredMixin, View):
    def get(self, request, id):
        copy = Copy.objects.get(id=id)
        book = Copy.book.__get__(copy)

        context = {}
        context['copy'] = copy
        context['book'] = book
        return render(request, 'member/copyView.html', context)
    
    def post(self, request, id):
        user = request.user
        copy = Copy.objects.get(id=id)
        member = Member.objects.get(userObj=user)
        book = copy.book
        context = {}
        context['copy'] = copy
        context['member'] = member
        numAlreadyIssued = Copy.objects.filter(issuedTo=member).count()

        if numAlreadyIssued >= 3:
            messages.error(request, 'You have already issued 3 books. Return them to issue this book')
            return redirect(reverse('memBookList'))

        if copy.isIssued:
            messages.error(request, 'This copy has already been issued to another user. Select another copy')
            return redirect(reverse('memBookView', args=[book.id]))
        else:
            copy.isIssued = True
            copy.issueDate = DT.date.today()
            copy.returnDate = DT.date.today() + DT.timedelta(days=7)
            copy.issuedTo = member
            copy.save()
            return redirect(reverse('memBookList'))
    

class IssuedList(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        member = Member.objects.get(userObj=user)
        copyList = Copy.objects.filter(issuedTo=member)
        context = {}
        context['copyList'] = copyList
        return render(request, 'member/issuedList.html', context)

class ReturnCopy(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user
        member = Member.objects.get(userObj=user)
        copy = Copy.objects.get(id=id)
        unconfirmedReturns = ''
        if VerifyReturns.objects.filter(copy=copy).exists():
            unconfirmedReturns = VerifyReturns.objects.get(copy=copy)
        if not copy.issuedTo == member:
            messages.error(request, 'Do not attempt to change the URL to manipulate Returns. Your activity will be reported to the librarian')
            return redirect(reverse('memberDash'))

        context={}
        context['copy'] = copy
        context['unconfirmedReturns'] = unconfirmedReturns
        return render(request, 'member/returnBook.html', context)

    def post(self, request, id):
        user = request.user
        member = Member.objects.get(userObj=user)
        copy = Copy.objects.get(id=id)
        
        if not copy.issuedTo == member:
            messages.error(request, 'Do not attempt to change the URL to manipulate Returns. Your activity will be reported to the librarian')
            return redirect(reverse('memberDash'))
        
        if VerifyReturns.objects.filter(copy=copy).exists():
            messages.warning(request, 'You have already issued a return request for this book. Awaiting librarian approval')
            return redirect(reverse('memIssueList'))

        if PendingFines.objects.filter(copy=copy).exists():
            messages.warning(request, 'You have already issued a return request for this book. Awaiting librarian approval')
            return redirect(reverse('memIssueList'))

        if DT.date.today() <= copy.returnDate:
            newReturn = VerifyReturns.objects.create(copy=copy, returnDate=DT.date.today(), member=member)
            newReturn.save()
            messages.info(request, 'Your return has been noted. Awaiting librarian approval')
        else:
            PendingFines.objects.create(copy=copy, returnDate=DT.date.today(), member=member).save()
            messages.info(request, 'Your return was late. Awaiting librarian approval for fine receipt')
        return redirect(reverse('memberDash'))

class PendingApprovals(View):
    def get(self, request):
        user = request.user
        member = Member.objects.get(userObj=user)
        pendingRequests = VerifyReturns.objects.filter(member=member)
        context = {}
        context['pendingRequests'] = pendingRequests

        return render(request, 'member/pendingApprovals.html', context)

class PendingFinesView(View):
    def get(self, request):
        user = request.user
        member = Member.objects.get(userObj=user)
        pendingFines = PendingFines.objects.filter(member=member)
        context = {}
        context['pendingFines'] = pendingFines

        return render(request, 'member/pendingFines.html', context)

class PayFines(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        member = Member.objects.get(userObj=user)
        pendingFines = PendingFines.objects.filter(member=member)
        context = {}
        context['pendingFines'] = pendingFines
        return render(request, 'member/payFines.html', context)

    def post(self, request):
        user = request.user
        member = Member.objects.get(userObj=user)