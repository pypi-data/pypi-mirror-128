from django.contrib import admin
from django.contrib.auth import models

from accounts.models import User, Verification
from accounts.forms import UserCreationForm


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_admin')



class VerifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account_code', 'verify_code')


admin.site.register(User, UserAdmin)
admin.site.register(Verification, VerifyAdmin)
