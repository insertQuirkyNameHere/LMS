from django.urls import path
from .views import (Dashboard, AccountManagement, DeleteAccount, LibrarianAccountManagement, AddLibrarian, DeleteLibrarian,
    MemberAccountManagement, AddMember, DeleteMember)
urlpatterns = [
    path('', Dashboard.as_view(), name='adminDash'),
    path('accounts/', AccountManagement.as_view(), name='adminAccManage'),
    path('accounts/librarian/', LibrarianAccountManagement.as_view(), name='adminLibAccManage'),
    path('accounts/librarian/add/', AddLibrarian.as_view(), name='adminLibAccAdd'),
    path('accounts/librarian/del/', DeleteLibrarian.as_view(), name='adminLibAccDel'),
    path('accounts/del/<int:id>/', DeleteAccount.as_view(), name='adminAccDel'),
    path('accounts/member/', MemberAccountManagement.as_view(), name='adminMemberAccManage'),
    path('accounts/member/add/', AddMember.as_view(), name='adminMemberAccAdd'),
    path('accounts/member/del/', DeleteMember.as_view(), name='adminMemberAccDel'),
]