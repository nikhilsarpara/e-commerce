from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.


class account_manager(BaseUserManager):
    def create_user(self,email,username,firstname,lastname,phone,password=None):
        user = self.model(
            email = self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,email,username,firstname,lastname,phone,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self.db)
        return user


class registration(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
    objects = account_manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','firstname','lastname','phone']

    def has_module_perms(self,add_label):
        return True
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(registration, on_delete=models.CASCADE)
    profile_image =  models.ImageField(upload_to="Profile_Pic")