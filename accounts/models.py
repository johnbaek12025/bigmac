from re import L
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class UserManager(BaseUserManager):
    #BaseUserManager provides flexibility with adding parameter what need to be
    def create_user(self, first_name, last_name, username, email, password=None):        
        """
        self.normalize_email(email)
        It will take the email address from you.
        For example, if you give any uppercase email address, it will take your uppercase email address and
        convert it into the lowercase.

        user.set_password(pwd)
        It will take the password and encode the password and store it in the database.
        So that's why whenever storing the password, use a set_password because
        cannot store the password in a plaintext.

        user.save(using=self._db)
        while saving the user, using equal to self._db
        Django by default uses using parameter to define which database the manager should use for the operation
        so this is mostly used in case if you have multiple databases by which you define which db need to us for this operation.

        but in this case there is only one db so self._db is pointing to current database
        """
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email), 
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Abstract base user, we are going to extend it in the user class.
    So by extending this abstract user or I can say by inheriting this abstract base user, 
    we are taking the full control of editing the whole custom user mode l, 
    including the authentication functionality of Django.

    if Abstract user is used, Django won't give up the full control over its user model
    it is only allowable about add extra fields, that is it.

    In this project there are three role, one is customer, another one is restaurant role and the other is admin role

    While creating a custom user model, we need to take care of the Django's required field 
    so the required fields are actually required field.
    """ 
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Restaurant'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #Authentication part of the Django custom user
    #Abstract based user gives the ability to set the user name field as default.
    # Django uses username as a login field
    # But in this override to email
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager() # this manager is nothing but this class and another one are in the settings file

    def __str__(self):
        return self.email
    
    """
    return to if the user is an active superuser or is an admin
    and for inactive users it will be always it will return False

    That means by default, admin and super admin can only have the access to this model

    for permistion there are two steps more
    one is needed to tell this user class that which user manages to use on this model

    """    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):        
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'        
        return user_role


class UserProfile(models.Model):
    #warranty to the User
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='user/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    coutnry = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=15, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'

    def __str__(self):
        return self.user.email