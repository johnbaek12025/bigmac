from django import forms
from .models import Vendor
"""
About django model forms
It is a feature built in of Django and it provides the replica of model fields
And DJango forms are very simple and secure as well
So to implement Django form in a application, simply needed to create Django form.py
and create form class and call that form from views and render it inside HTML templates
"""

class VendorForm(forms.ModelForm):
    class Meta:
         model = Vendor
         fields = ['vendor_name', 'vendor_license']