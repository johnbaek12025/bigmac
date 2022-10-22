from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from accounts.form import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages
from django.contrib import auth
from .utility import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from vendor.form import VendorForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


#Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

#Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(req):
    if req.user.is_authenticated:
        messages.warning(req, 'You are already logged in!')
        return redirect('myAccount')
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            mail_url = 'accounts/emails/account_verification_email.html'
            send_verification_email(req, user, mail_subject, mail_url)
            
            messages.success(req, 'Your account has been registered successfully~')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(req, 'accounts/registerUser.html', context)


def registerVendor(req):
    if req.method == 'POST':
        #store the data and create the user        
        form = UserForm(req.POST)
        v_form = VendorForm(req.POST, req.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            # Send verification email
            mail_subject = 'Please activate your account'
            mail_url = 'accounts/emails/account_verification_email.html'
            send_verification_email(req, user, mail_subject, mail_url)
            messages.success(req, 'Your account has been registered successfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context ={
        'form': form,
        'v_form': v_form,
    }

    return render(req, 'accounts/registerVendor.html', context=context)


def activate(req, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(req, 'You got activation of your account.')
        return redirect('myAccount')
    else:
        messages.error(req, 'Invalid activation link')
        return redirect('myAccount')


def login(req):
    if req.user.is_authenticated:
        messages.warning(req, 'You are already logged in!')
        return redirect('myAccount')
    elif req.method == 'POST':
        email = req.POST['email']
        password = req.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(req, user)
            messages.success(req, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(req, 'Invalid login credentials')
            return redirect('login')
    return render(req, 'accounts/login.html')


def logout(req):
    auth.logout(req)
    messages.info(req, "You are logged out.")    
    return redirect('login')


@login_required(login_url='login')
def myAccount(req):
    user = req.user
    redirectUrl = detectUser(user)
    print(redirectUrl)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(req):
    return render(req, 'accounts/custDashboard.html')


@user_passes_test(check_role_vendor)
@login_required(login_url='login')
def vendorDashboard(req):
    return render(req, 'accounts/vendorDashboard.html')


def forgot_password(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)            
            #send reset password email
            mail_subject = 'Reset your password'
            mail_url = 'accounts/emails/reset_password_email.html'
            send_verification_email(req, user, mail_subject, mail_url)

            messages.success(req, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else: # email object is not exist in User
            messages.error(req, 'Account does not exist')
            return redirect('login')
    return render(req, 'accounts/forgot_password.html')


def reset_password_validate(req, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return 


def reset_password(req):
    return render(req, 'accounts/reset_password.html')