from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, default='admin')
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    otpCode = models.CharField(max_length=4 ,blank=True,null=True)


    REQUIRED_FIELDS = [ 'email']

    def __str__(self):
        return self.username

from django.db import models

class PesEvents(models.Model):
    eventID = models.BigAutoField(primary_key=True)
    OLDdID = models.IntegerField(null=True)
    FSPID = models.IntegerField()
    eventdate = models.DateTimeField(default=timezone.now)
    d_First = models.CharField(max_length=75)
    d_middle_a = models.CharField(max_length=75, null=True)
    d_middle_b = models.CharField(max_length=75, null=True)
    d_Last = models.CharField(max_length=125)
    d_Maiden = models.CharField(max_length=125, null=True)
    d_Address = models.CharField(max_length=255)
    d_Unit = models.CharField(max_length=50, null=True)
    d_City = models.CharField(max_length=125)
    d_Prov = models.CharField(max_length=3)
    d_Postal = models.CharField(max_length=12)
    d_AreaCode = models.IntegerField(null=True)
    d_exchange = models.IntegerField(null=True)
    d_phone = models.CharField(max_length=4, null=True)
    d_DOB = models.DateField()
    d_birth_Country = models.CharField(max_length=125)
    d_birth_City = models.CharField(max_length=125, null=True)
    d_birth_Prov = models.CharField(max_length=3, null=True)
    d_DOD = models.DateField()
    d_death_Country = models.CharField(max_length=125)
    d_death_City = models.CharField(max_length=125, null=True)
    d_death_Prov = models.CharField(max_length=3, null=True)
    d_SIN = models.CharField(max_length=11, null=True)
    d_PHC = models.CharField(max_length=50, null=True)
    d_Prov_PHC = models.CharField(max_length=3, null=True)
    d_BCN = models.CharField(max_length=255, null=True)
    d_death_age = models.IntegerField()
    d_disp_Name = models.CharField(max_length=275, null=True, blank=True)
    d_disp_Postal = models.CharField(max_length=12,null=True)
    d_dispdate = models.DateField(null=True)
    e_Salutation = models.CharField(max_length=12, null=True)
    e_First = models.CharField(max_length=75)
    e_Initial = models.CharField(max_length=75, null=True)
    e_Last = models.CharField(max_length=125)
    e_Address = models.CharField(max_length=255)
    e_Unit = models.CharField(max_length=50, null=True)
    e_City = models.CharField(max_length=125)
    e_Prov = models.CharField(max_length=3)
    e_Postal = models.CharField(max_length=12)
    e_AreaCode = models.IntegerField(null=True)
    e_exchange = models.IntegerField(null=True)
    e_phone_4 = models.CharField(max_length=4)
    e_relationship = models.CharField(max_length=50)
    ExecutorID = models.IntegerField(null=True)
    FaxDate = models.DateField(null=True)
    ReportDate = models.DateField(null=True)
    Status = models.CharField(max_length=50, null=True)
    notes = models.CharField(max_length=600, null=True)
    DignityPlan = models.SmallIntegerField(null=True)
    Contract = models.CharField(max_length=125, null=True)
    e_email = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'PesEvents'

class PesExecutor(models.Model):
    ExecutorID = models.BigAutoField(primary_key=True)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Status = models.IntegerField()
    ExecutorOverrideID = models.IntegerField(null=True, blank=True)
    LastAccessed = models.DateTimeField(null=True, blank=True)
    LoginCount = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    LanguageID = models.CharField(max_length=2, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'PesExecutor'