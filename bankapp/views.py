from django.shortcuts import render
from . models import Account
import random
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    return render(request,"index.html")
def createaccount(request):
    return render(request,"createaccount.html")
def create(request):
    acno=''
    for i in range(6):
        acno=acno+str(random.randint(1,9))
    acno=int(acno)
    name=request.POST['name']
    gender=request.POST['gender']
    address=request.POST['address']
    contactno=request.POST['contactno']
    emailaddress=request.POST['emailaddress']
    panno=request.POST['panno']
    aadharno=request.POST['aadharno']
    balance=request.POST['balance']
    password=request.POST['password']
    ac=Account(acno=acno,name=name,gender=gender,address=address,contactno=contactno,emailaddress=emailaddress,panno=panno,aadharno=aadharno,balance=balance,password=password)
    ac.save()
    msg='Your account no is='+str(acno)
    return render(request,"index.html",{'msg':msg})
def login(request):
    return render(request,"login.html")
def logcode(request):
    acno=request.POST['acno']
    password=request.POST['password']
    operation=request.POST['operation']
    msg=''
    try:
        obj=Account.objects.get(acno=acno,password=password)
        if operation=="Deposit":
            acno=obj.acno
            request.session['acno']=acno
            return render(request,"deposit.html")
        elif operation=="Withdraw":
            acno=obj.acno
            request.session['acno']=acno
            return render(request,"withdraw.html")
        elif operation=="Transfer":
            acno=obj.acno
            request.session['acno']=acno
            return render(request,"transfer.html")
        elif operation=="Enquiry":
            balance=obj.balance
            msg='Your balance='+str(balance)
            return render(request,"index.html",{'msg':msg})
    except ObjectDoesNotExist:
        msg='Invalid Account No'
    return render(request,"login.html",{'msg':msg})
def depositamt(request):
    amt=int(request.POST['amt'])
    obj=Account.objects.get(acno=request.session['acno'])
    balance=obj.balance
    balance=balance+amt
    acno=obj.acno
    Account.objects.filter(pk=acno).update(balance=balance)
    msg='Amount is credited'
    request.session['acno']=None
    return render(request,"index.html",{'msg':msg})
def withdrawamt(request):
    amt=int(request.POST['amt'])
    obj=Account.objects.get(acno=request.session['acno'])
    balance=obj.balance
    msg=''
    if balance<amt:
        msg=msg+'Insufficent Balance.'
        return render(request,"index.html",{'msg':msg})
    balance=balance-amt
    acno=obj.acno
    Account.objects.filter(pk=acno).update(balance=balance)
    msg=msg+'Amount is debited'
    request.session['acno']=None
    return render(request,"index.html",{'msg':msg})
def transferamt(request):
    bacno=request.POST['bacno']
    amt=int(request.POST['amt'])
    msg=''
    try:
        obj2=Account.objects.get(acno=bacno)
        obj1=Account.objects.get(acno=request.session['acno'])
        balance1=obj1.balance
        if balance1<amt:
            msg=msg+'Insufficient balance'
            return render(request,"index.html",{'msg':msg})
        balance1=balance1-amt
        balance2=obj2.balance
        balance2=balance2+amt
        Account.objects.filter(pk=obj1.acno).update(balance=balance1)
        Account.objects.filter(pk=obj2.acno).update(balance=balance2)
        msg=msg+'Fund is transferred'
        return render(request,"index.html",{'msg':msg})
    except ObjectDoesNotExist:
        msg=msg+'Benificary account is invalid'
    return render(request,"index.html",{'msg':msg})