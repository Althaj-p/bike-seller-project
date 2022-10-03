import re
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import requests

# Create your views here.
def user_login(request):
    error=""
    if request.method=='POST':
        e=request.POST['email']
        p=request.POST['password']
        user=authenticate(username=e,password=p)
        if user:
            login(request, user)
            return redirect('index')
        else:
           error="yes"
    d={'error':error} 
    return render(request,'login.html',d)
def register(request):
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        p=request.POST['pwd']
        cp=request.POST['cpwd']
        m=request.POST['mobile']
        lc=request.POST['location']
        u=request.POST['uname']
        if p==cp:
            if User.objects.filter(username=e).exists():
                error="yes"
            else:
                user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
                obj=reg_tbl.objects.create(user=user,user_name=u,location=lc,mobile=m)
                obj.save()
                error="no"
                return redirect('login')
        else:
            error="not"
    d={'error':error}    
    return render(request,'register.html',d)
def index(request):
    obj=bikes.objects.all()
    return render(request,'index.html',{'bikes':obj})
def user_logout(request):
    # user=request.user
    logout(request)
    return redirect('index')
def companies(request):
    companies=company.objects.all()
    return render(request,'companies.html',{'companies':companies})
def all_bikes(request):
    obj=bikes.objects.filter(available=True)
    return render(request,'all_bikes.html',{'bikes':obj})
def companiesview(request,slug):
    # if(company.objects.filter(slug=slug)):
    obj=bikes.objects.filter(company__slug=slug,available=True)
    company_name=company.objects.filter(slug=slug).first() #for display company name on heading
    d={'bikes':obj,'company_name':company_name}
    return render(request,"companies_view.html",d)
    # else:
    #     messages.info(request,'No such compamies found')
    #     return redirect('companies')
def bike_view(request,cat_slug,prod_slug):
    if(company.objects.filter(slug=cat_slug)):
        if(bikes.objects.filter(slug=prod_slug,available=True)):
            obj=bikes.objects.filter(slug=prod_slug,available=True).first()
            context={'bikes':obj}
        else:
            messages.error(request,'No such bikes found')
            return redirect('companiesview')
    else:
        messages.error(request,'no category found')
        return redirect('companiesview')
    return render(request,'detail.html',context)
def apishow(request):

    url = "https://motorcycle-specs-database.p.rapidapi.com/make/Aprilia/model/Dorsoduro%201200"
    # url = "https://motorcycle-specs-database.p.rapidapi.com/make/yamaha/model/yfz"
    # url = "https://motorcycle-specs-database.p.rapidapi.com/model/make-name/Yamaha"
    headers = {
	    "X-RapidAPI-Key": "ebdb0737b0mshf5c866d8cfa9872p1cb608jsn6f53bc670c82",
	    "X-RapidAPI-Host": "motorcycle-specs-database.p.rapidapi.com"
    }

    data = requests.request("GET", url, headers=headers).json()
    response=data[0]['articleCompleteInfo']

    # data=response.json()
    # aa=data['articleCompleteInfo']

    # print(response.text)
    return render(request,'api.html',{'response':response,'data':data})
