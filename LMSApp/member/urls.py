from django.urls import path
from .views import *

urlpatterns=[
    path('', Dashboard.as_view(), name='memberDash'),
    path('books/', BookList.as_view(), name='memBookList'),
    path('books/<int:id>/', BookView.as_view(), name='memBookView'),
    path('copy/<int:id>/', CopyView.as_view(), name='memCopyView'),
    path('issuedBooks/', IssuedList.as_view(), name='memIssueList'),
]