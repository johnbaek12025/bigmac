from atexit import register
from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

"""
how to make this password field with non editable by default.
when a custom user model created, password will be its own password field and
will be created as it can be edited from the panel.

But for prohibition from editing, simply need to specify some rules so that it will be marked as non editable field in from the backend.
first, Having to be done is acutually the current account must be the user admin.
It will come from django.contrib.auth.admin import UserAdmin
"""

class CustomUserAdmin(UserAdmin):
    """
    Tuples are immutable sequences in Python. 
    if you write only one object in parentheses (), the parentheses () are ignored and not treated as a tuple.    
    To generate a tuple with one element, a comma , is required at the end.    
    """
    list_display = ("email", "password", 'username', 'role', 'is_active')
    ordering = ('-created_date',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
 