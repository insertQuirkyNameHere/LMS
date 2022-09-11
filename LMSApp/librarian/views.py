from multiprocessing import context
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from models.models import *
# Create your views here.

class DashBoard(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_lib:
            return render(request, 'librarian/dashboard.html')
        else:
            messages.error(request, 'You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class VerifyReturnRequests(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_member:
            pendingReturnRequests = VerifyReturns.objects.all()
            pendingFines = PendingFines.objects.all()
            context = {}
            context['pendingRequests'] = pendingReturnRequests
            context['pendingFines'] = pendingFines
            return render(request, 'librarian/verifyReturns.html', context)
        
        else:
            messages.error(request, 'You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request):
        if not request.user.is_member:
            if 'approve' in request.POST:
                id = request.POST['approve']
                returnRequest = VerifyReturns.objects.get(id=id)
                member = returnRequest.member
                returnedDate = returnRequest.returnDate
                copy = returnRequest.copy
                dueDate = copy.returnDate
                
                if returnedDate <= dueDate:
                    BorrowHistory.objects.create(copy = copy, borrower=member, borrowDate=copy.issueDate, returnedDate=returnedDate).save()

                    copy.isIssued = False
                    copy.issuedTo = None
                    copy.issueDate = None
                    copy.returnDate = None
                    copy.save()
                    returnRequest.delete()

            elif 'reject' in request.POST:
                id = request.POST['reject']
                VerifyReturns.objects.get(id=id).delete()

            return redirect(reverse('verifyReturns'))
    
                
        else:
            messages.error(request, 'You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class VerifyFine(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_member:
            if 'approve' in request.POST:
                id = request.POST['approve']
                returnRequest = PendingFines.objects.get(id=id)
                member = returnRequest.member
                returnedDate = returnRequest.returnDate
                copy = returnRequest.copy
                dueDate = copy.returnDate
                fine = 5 * ((returnedDate-dueDate).days)

                borrowObj = BorrowHistory.objects.create(copy = copy, borrower=member, borrowDate=copy.issueDate, returnDate=returnedDate)
                borrowObj.save()
                FinesHistory.objects.create(borrowInstance=borrowObj, dueDate=dueDate, amount=fine).save()

                copy.isIssued = False
                copy.issuedTo = None
                copy.issueDate = None
                copy.returnDate = None
                copy.save()
                returnRequest.delete()

            elif 'reject' in request.POST:
                id = request.POST['reject']
                PendingFines.objects.get(id=id).delete()
            
            return redirect(reverse('verifyReturns'))

class ViewBorrowHistory(View):
    def get(self, request):
        borrowList = BorrowHistory.objects.all()
        context = {}
        context['borrowList'] = borrowList
        return render(request, 'librarian/borrowHistory.html', context)

class ViewFineHistory(View):
    def get(self, request):
        fineList = FinesHistory.objects.all()
        context = {}
        context['fineList'] = fineList
        return render(request, 'librarian/fineHistory.html', context)



        