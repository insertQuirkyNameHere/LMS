
from copy import copy
from multiprocessing import context
from urllib import request
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import (AddLibrarianForm, AddBookForm, EditBookForm, AddCopiesForm,
    EditCopiesForm)
from models.models import Librarian, Member, Book, Author, Genre, Copy
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
        if request.user.is_admin or request.user.is_lib:
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
        if request.user.is_admin or request.user.is_lib:
            userObj = UserModel.objects.get(id=id)
            if (Librarian.objects.filter(userObj=userObj).exists()):
                if request.user.is_admin:
                    Librarian.objects.get(userObj=userObj).delete()
                    userObj.delete()
                    messages.info(request, 'Librarian User deleted successfully')
                    return redirect(reverse('adminAccManage'))
                else:
                    messages.error(request, 'Librarian Users do no have authorization to remove other librarians')

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
        if request.user.is_admin or request.user.is_lib:
            return render(request, 'admin/member/MemberManager.html')

        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('adminAccManage'))

class AddMember(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin or request.user.is_lib:
            memberList = PendingMemberAccounts.objects.all()
            context = {}
            context['memberList'] = memberList
            return render(request, 'admin/member/addMember.html', context)

        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request):
        if request.user.is_admin or request.user.is_lib:
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
        if request.user.is_admin or request.user.is_lib:
            memberAccList = Member.objects.all()
            context = {}
            context['memberAccList'] = memberAccList
            return render(request, 'admin/member/delMember.html', context)
            
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class BookManagement(View):
    def get(self, request):
        if not request.user.is_member:
            return render(request, 'admin/book/bookManager.html')
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class BookList(View):
    def get(self, request):
        if not request.user.is_member:
            bookList = Book.objects.all()
            context = {}
            context['bookList'] = bookList
            return render(request, 'admin/book/bookList.html', context)
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request):
        if not request.user.is_member:
            if 'del' in request.POST:
                return redirect(reverse('delBooks', args=(request.POST['del'])))

            elif 'edit' in request.POST:
                return redirect(reverse('editBooks', args=(request.POST['edit'])))
                
            return(redirect(reverse('bookList')))
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class AddBooks(View):
    def get(self, request):
        if not request.user.is_member:
            form = AddBookForm()
            authorList = Author.objects.all()
            genreList = Genre.objects.all()
            context = {}
            context['form'] = form
            context['authorList'] = authorList
            context['genreList'] = genreList
            return render(request, 'admin/book/addBooks.html', context)
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request):
        if not request.user.is_member:
            form = AddBookForm(request.POST)

            if form.is_valid():
                author = form.cleaned_data['authors']
                authorList = author.split(',')

                for i in range (0, len(authorList)):
                    authorList[i] = authorList[i].strip()
                    authorList[i] = authorList[i].lower()
                    tempStr = ""
                    tempStr += authorList[i][0].upper()
                    j = 1

                    while(j<len(authorList[i])):
                        tempStr += authorList[i][j]
                        if(authorList[i][j] == ' '): 
                            j=j+1
                            tempStr += authorList[i][j].upper()
                        j+=1
                    authorList[i] = tempStr


                genre = form.cleaned_data['genre']
                genreList = genre.split(',')

                for i in range (0, len(genreList)):
                    genreList[i] = genreList[i].strip()
                    genreList[i] = genreList[i].lower()
                    tempStr = ""
                    tempStr += genreList[i][0].upper()
                    j = 1

                    while(j<len(genreList[i])):
                        tempStr += genreList[i][j]
                        if(genreList[i][j] == ' '): 
                            j=j+1
                            tempStr += genreList[i][j].upper()
                        j+=1
                    genreList[i] = tempStr

                bookName = form.cleaned_data['title']
                if Book.objects.filter(title=bookName).exists():
                    messages.info(request, 'The book you\'re trying to add already exists')
                else:
                    book = Book.objects.create(title=bookName)
                    book.save()

                    for i in authorList:
                        if Author.objects.filter(name=i).exists():
                            book.authors.add(Author.objects.get(name=i))
                        else:
                            newAuthor = Author.objects.create(name=i)
                            newAuthor.save()
                            book.authors.add(newAuthor)

                    for i in genreList:
                        if Genre.objects.filter(genre=i).exists():
                            book.genre.add(Genre.objects.get(genre=i))
                        else:
                            newGenre = Genre.objects.create(genre=i)
                            newGenre.save()
                            book.genre.add(newGenre)

                return redirect(reverse('bookManage'))
            
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class DelBooks(View):
    def get(self, request, id):
        if not request.user.is_member:
            bookToDel = Book.objects.get(id=id)
            context = {}
            context['book'] = bookToDel
            return render(request, 'admin/book/delBook.html', context)
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request, id):
        if not request.user.is_member:
            bookToDel = Book.objects.get(id=id)
            bookToDel.delete()
            return redirect(reverse('bookList'))
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class EditBooks(View):
    def get(self, request, id):
        if not request.user.is_member:
            bookToEdit = Book.objects.get(id=id)
            genreList = []
            authorsList = []
            for genre in bookToEdit.genre.all():
                genreList.append(genre.genre)

            for author in bookToEdit.authors.all():
                authorsList.append(author.name)

            form = EditBookForm({
                'title' : bookToEdit.title,
                'authors': ', '.join(authorsList),
                'genre': ', '.join(genreList),
            })
            
            copyForm = AddCopiesForm()
            allGenres = Genre.objects.all()
            allAuthors = Author.objects.all()
            issuedCopies = bookToEdit.copy_set.filter(isIssued=True)
            unissuedCopies = bookToEdit.copy_set.filter(isIssued=False)

            context = {}
            context['book'] = bookToEdit
            context['form'] = form
            context['copyForm'] = copyForm
            context['authorList'] = allAuthors
            context['genreList'] = allGenres
            context['issuedCopies'] = issuedCopies
            context['unissuedCopies'] = unissuedCopies
            return render(request, 'admin/book/editBook.html', context)
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request, id):
        if not request.user.is_member:
            bookForm = EditBookForm(request.POST)
            bookToEdit = Book.objects.get(id=id)
            if bookForm.is_valid():
                title = bookForm.cleaned_data['title']
                authors = bookForm.cleaned_data['authors']
                genre = bookForm.cleaned_data['genre']  

                if authors:
                    bookToEdit.authors.clear()
                    authorList = authors.split(',')
                    for i in range (0, len(authorList)):
                        authorList[i] = authorList[i].strip()
                        authorList[i] = authorList[i].lower()
                        tempStr = ""
                        tempStr += authorList[i][0].upper()
                        j = 1

                        while(j<len(authorList[i])):
                            tempStr += authorList[i][j]
                            if(authorList[i][j] == ' '): 
                                j=j+1
                                tempStr += authorList[i][j].upper()
                            j+=1
                        authorList[i] = tempStr
                    
                    for i in authorList:
                        if Author.objects.filter(name=i).exists():
                            bookToEdit.authors.add(Author.objects.get(name=i))
                        else:
                            newAuthor = Author.objects.create(name=i)
                            newAuthor.save()
                            bookToEdit.authors.add(newAuthor)

                if genre:
                    bookToEdit.genre.clear()
                    genreList = genre.split(',')

                    for i in range (0, len(genreList)):
                        genreList[i] = genreList[i].strip()
                        genreList[i] = genreList[i].lower()
                        tempStr = ""
                        tempStr += genreList[i][0].upper()
                        j = 1

                        while(j<len(genreList[i])):
                            tempStr += genreList[i][j]
                            if(genreList[i][j] == ' '): 
                                j=j+1
                                tempStr += genreList[i][j].upper()
                            j+=1
                        genreList[i] = tempStr

                    for i in genreList:
                        if Genre.objects.filter(genre=i).exists():
                            bookToEdit.genre.add(Genre.objects.get(genre=i))
                        else:
                            newGenre = Genre.objects.create(genre=i)
                            newGenre.save()
                            bookToEdit.genre.add(newGenre)

                if title:
                    bookToEdit.title = title

                bookToEdit.save()
                return redirect(reverse('bookList'))

            else:
                messages.error(request, 'Invalid form Data, please follow constraints')
                return redirect(reverse('editBooks', args=(id)))     
        
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class AddCopy(View):
    def post(self, request, id):
        if not request.user.is_member:
            form = AddCopiesForm(request.POST)
            book = Book.objects.get(id=id)
            if form.is_valid():
                numOfCopies = form.cleaned_data['numOfCopies']
                price = form.cleaned_data['price']
                for i in range(0, numOfCopies):
                    newCopy = Copy.objects.create(book=book, price=price)
                    newCopy.save()
                    messages.info(request, str(numOfCopies)+' Copies Have been added')
                    return redirect(reverse('editBooks', args=(id)))
            else:
                messages.error(request, 'Invalid form Data, please follow constraints')
                return redirect(reverse('editBooks', args=(id)))     
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class BookView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        issuedCopies = book.copy_set.filter(isIssued=True)
        unissuedCopies = book.copy_set.filter(isIssued=False)

        copyForm = AddCopiesForm()
        context = {}
        context['book'] = book
        context['issuedCopies'] = issuedCopies
        context['unissuedCopies'] = unissuedCopies
        context['copyForm'] = copyForm
        return render(request, 'admin/book/bookView.html', context)
        
class CopyManagement(View):
    def get(self, request, id):
        if not request.user.is_member:
            copy = Copy.objects.get(id=id)
            context= {}
            context['copy'] = copy
            return render(request, 'admin/book/copyManagement.html', context)
            
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

class EditCopy(View):
    def get(self, request, id):
        if not request.user.is_member:
            copyToEdit = Copy.objects.get(id=id)
            form = EditCopiesForm({
                'price': copyToEdit.price,
                'isIssued': copyToEdit.isIssued,
                'issuedDate': copyToEdit.issueDate,
                'returnDate': copyToEdit.returnDate,
            })
            context = {}
            context['copy'] = copyToEdit
            context['form'] = form
            return render(request, 'admin/book/editCopy.html', context)
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))
    
    def post(self, request, id):
        if not request.user.is_member:
            copyToEdit = Copy.objects.get(id=id)
            form = EditCopiesForm(request.POST)

            if form.is_valid():
                if 'del' in request.POST:
                    print('Hello')
                price = form.cleaned_data['price']
                isIssued = form.cleaned_data['isIssued']
                issuedDate = form.cleaned_data['issuedDate']
                returnDate = form.cleaned_data['returnDate']

                if price:
                    copyToEdit.price = price
                
                if isIssued:
                    copyToEdit.isIssued = True
                    if issuedDate:
                        copyToEdit.issueDate = issuedDate
                    else:
                        messages.error(request, 'Copy cannot be set to issued without Issue Date and Return Date')
                        return redirect(reverse('editCopies', args=(id)))
                
                    if returnDate:
                        copyToEdit.returnDate = returnDate
                    else:
                        messages.error(request, 'Copy cannot be set to issued without Issue Date and Return Date')
                        return redirect(reverse('editCopies', args=(id)))

            else:
                messages.error(request, 'Invalid form Data, please follow constraints')
                return redirect(reverse('editCopies', args=(id)))

            messages.info(request, 'Copy has been edited')
            return redirect(reverse('editBooks', args=(copyToEdit.book.id)))  

        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))    

class DeleteCopy(View) :
    def get(self, request, id):
        if not request.user.is_member:
            copyToDelete = Copy.objects.get(id=id)
            context = {}
            context['copy'] = copyToDelete
            return render(request, 'admin/book/delCopy.html', context)
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))

    def post(self, request, id):
        if not request.user.is_member:
            copyToDelete = Copy.objects.get(id=id)
            bookId = Copy.book.__get__(copyToDelete).id
            copyToDelete.delete()
            messages.info(request, 'Copy was deleted')
            return redirect(reverse('viewBook', args=[bookId]))
        else:
            messages.error('You do not have authorization to view that page')
            return redirect(reverse('userScramble'))