from django.urls import path
from .views import *

urlpatterns=[
    path('', Dashboard.as_view(), name='memberDash'),
    path('books/', BookList.as_view(), name='memBookList'),
    path('books/<int:id>/', BookView.as_view(), name='memBookView'),
    path('copy/<int:id>/', CopyView.as_view(), name='memCopyView'),
    path('issuedBooks/', IssuedList.as_view(), name='memIssueList'),
    path('returnBook/<int:id>/', ReturnCopy.as_view(), name='memReturnBook'),
    path('pendingApprovals/', PendingApprovals.as_view(), name='memPendingApprovals'),
    path('pendingFines/', PendingFinesView.as_view(), name='memPendingFines'),
    path('borrowHistory/', ViewBorrowHistory.as_view(), name='memBorrowHistory'),
    path('fineHistory/', ViewFinesHistory.as_view(), name='memFineHistory'),
]