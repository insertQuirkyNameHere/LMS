import datetime as DT

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View

from models.models import Book, Copy, Member

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
        print('Copy:', copy)
        print('Member:', member)
        print('numIssued:', numAlreadyIssued, '\n')
        pass

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
    pass

class IssuedBookView(View):
    pass
