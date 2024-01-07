from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from datetime import datetime
from django.core.validators import MinValueValidator

# Create your models here.

class Activemanager(models.Manager):
    def active(self):
        return self.filter(active=True) 

    

class usermanager(BaseUserManager):
    use_in_migrations=True
    def _create_user(self,email,password,**extra_fields):
        if not email :
            raise ValueError("the given email must be set")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    def create_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        return self._create_user(email,password,**extra_fields)
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "superuser must have is_staff=True."
            )    
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "superuser must have is_superuser=True."
            )   
        return self._create_user(email,password,**extra_fields)



class user(AbstractUser) :
    username=None
    email=models.EmailField('email address',unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=usermanager()   


    
class producttagmanager(models.Manager):
    def get_by_natural_key(self,slug):
        return self.get(slug=slug)    
class producttag(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    objects=producttagmanager() 
    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)    
class product(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True
                           )
    name=models.CharField(max_length=32)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    slug=models.SlugField(max_length=48)
    active=models.BooleanField(default=True)
    in_stock=models.BooleanField(default=True)
    date_updated=models.DateTimeField(auto_now=True) 
    objects= Activemanager()
    tags= models.ManyToManyField(producttag,blank=True)
    def __str__(self) :
      return self.name
    


class notes(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    NOTE=models.CharField(max_length=100000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    def __str__(self):
        return ",".join(
            [
                self.NOTE,
                self.date,
                self.qr_code,
            ]
        )
             