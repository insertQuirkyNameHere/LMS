from django.contrib import admin
from .models import PendingMemberAccounts, CustomUser
# Register your models here.
admin.site.register(PendingMemberAccounts)
admin.site.register(CustomUser)
