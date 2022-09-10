from django.shortcuts import render
from django.views import View
# Create your views here.

class DashBoard(View):
    def get(self, request):
        return render(request, 'librarian/dashboard.html')
