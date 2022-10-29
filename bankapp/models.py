from django.db import models

# Create your models here.
class Account(models.Model):
    acno=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=6)
    address=models.TextField()
    contactno=models.CharField(max_length=15)
    emailaddress=models.EmailField(max_length=50)
    panno=models.CharField(max_length=10)
    aadharno=models.CharField(max_length=12)
    balance=models.IntegerField()
    password=models.CharField(max_length=20)



