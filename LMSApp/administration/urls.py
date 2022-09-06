from django.urls import path
from .views import (Dashboard, AccountManagement, DeleteAccount, LibrarianAccountManagement, AddLibrarian, DeleteLibrarian,
    MemberAccountManagement, AddMember, DeleteMember, BookManagement, BookList, BookView, AddBooks, DelBooks, EditBooks, AddCopy, EditCopy,
    CopyManagement)
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
    path('books/', BookManagement.as_view(), name='bookManage'),
    path('books/view', BookList.as_view(), name='bookList'),
    path('books/view/<int:id>/', BookView.as_view(), name='viewBook'),
    path('books/add', AddBooks.as_view(), name='addBooks'),
    path('books/del/<int:id>/', DelBooks.as_view(), name='delBooks'),
    path('books/edit/<int:id>/', EditBooks.as_view(), name='editBooks'),
    path('books/copy/<int:id>/ ', CopyManagement.as_view(), name='viewCopy'),
    path('books/copy/add/<int:id>/ ', AddCopy.as_view(), name='addCopies'),
    path('books/copy/edit/<int:id>/ ', EditCopy.as_view(), name='editCopies'),
    path('books/copy/del/<int:id>/ ', EditCopy.as_view(), name='delCopies'),
    
]