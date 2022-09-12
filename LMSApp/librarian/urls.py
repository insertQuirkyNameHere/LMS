from django.urls import path
from .views import *

urlpatterns = [
    path('', DashBoard.as_view(), name='libDash'),
    path('verifyReturns/', VerifyReturnRequests.as_view(), name='verifyReturns'),
    path('verifyFines/', VerifyFine.as_view(), name='verifyFines'),
    path('borrowHistory/', ViewBorrowHistory.as_view(), name='borrowHistory'),
    path('fineHistory/', ViewFineHistory.as_view(), name='fineHistory'),
]