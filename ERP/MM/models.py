from curses.ascii import isdigit
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

def validate_phone(string):
    if len(string) != 11:
        raise ValidationError("Enter a valid 11-digit phone number.")
    if string[0] != '1':
        raise ValidationError("Enter a valid phone number beginning with '1'.")
    for s in string:
        if not isdigit(s):
            raise ValidationError("There is a character in the phone number.")

def validate_digit(string):
    for s in string:
        if not isdigit(s):
            raise ValidationError("There is a non-digit character.")

class EUser(User):
    validate_phone = validate_phone
    # username, password, date_joined, email
    uid = models.AutoField(primary_key=True)
    sector = models.CharField(max_length=20)
    phone = models.CharField(max_length=11, validators=[validate_phone])
    question1 = models.CharField(max_length=50)
    answer1 = models.CharField(max_length=50)
    question2 = models.CharField(max_length=50)
    answer2 = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.username

class Vendor(models.Model):
    validate_phone = validate_phone
    validate_digit = validate_digit
    vid = models.AutoField(primary_key=True)
    euser = models.ForeignKey(to=EUser, on_delete=models.CASCADE)
    vname = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=50, blank=True)
    postcode = models.CharField(max_length=6, validators=[validate_digit])
    country = models.CharField(max_length=10)
    language = models.CharField(max_length=10)
    glAcount = models.CharField(max_length=6)
    phone = models.CharField(max_length=11, validators=[validate_phone], blank=True)
    fax = models.CharField(max_length=10, validators=[validate_digit], blank=True)
    tpType = models.CharField(max_length=1, blank=True)
    companyCode = models.CharField(max_length=4)
    pOrg = models.CharField(max_length=4)
    currency = models.CharField(max_length=10, blank=True)
    score = models.IntegerField(blank=True)

    def __str__(self) -> str:
        return self.vname + ', ' + self.city + ', ' + self.country
