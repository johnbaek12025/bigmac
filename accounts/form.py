from django import forms
from .models import User
"""
About django model forms
It is a feature built in of Django and it provides the replica of model fields
And DJango forms are very simple and secure as well
So to implement Django form in a application, simply needed to create Django form.py
and create form class and call that form from views and render it inside HTML templates
"""

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')        
        if password != confirm_password:
            raise forms.ValidationError("Password does not match~!")