from locale import currency
import re
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import requests
from . forms import *
import datetime
import razorpay
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

client=razorpay.Client(auth=('rzp_test_BSUvo0HwLizvLx','6ZJFYxSTNx5hplM4XjO6z953'))

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
    if not request.user.is_authenticated:
        return redirect('login')
    companies=company.objects.filter(available=True)
    return render(request,'companies.html',{'companies':companies})
def all_bikes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    obj=bikes.objects.filter(company__available=True,available=True)
    return render(request,'all_bikes.html',{'bikes':obj})
def companiesview(request,slug):
    if not request.user.is_authenticated:
        return redirect('login')
    # if(company.objects.filter(slug=slug)):
    obj=bikes.objects.filter(company__slug=slug,available=True)
    company_name=company.objects.filter(slug=slug).first() #for display company name on heading
    d={'bikes':obj,'company_name':company_name}
    return render(request,"companies_view.html",d)
    # else:
    #     messages.info(request,'No such compamies found')
    #     return redirect('companies')
def bike_view(request,cat_slug,prod_slug):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user
    userdata=reg_tbl.objects.get(user=user)
    email=userdata.user.username
    mobile=userdata.mobile

        
    if(company.objects.filter(slug=cat_slug)):
        if(bikes.objects.filter(slug=prod_slug,available=True)):
            obj=bikes.objects.filter(slug=prod_slug,available=True).first()
        else:
            messages.error(request,'No such bikes found')
            return redirect('companiesview')
    else:
        messages.error(request,'no category found')
        return redirect('companiesview')

    # user=request.user
    # userdata=reg_tbl.objects.get(user=user)
    n=obj.price
    order_amount=int(n*100)
    order_currency='INR'
    # client=razorpay.Client(auth=('rzp_test_BSUvo0HwLizvLx','6ZJFYxSTNx5hplM4XjO6z953'))
    payment_order=client.order.create({'amount':order_amount,'currency':order_currency,'payment_capture':'1'})
    payment_order_id=payment_order['id']
    context={'bikes':obj,'order_id':payment_order_id,'email':email,'mobile':mobile}
    return render(request,'detail.html',context)


def place_order(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    bike=bikes.objects.get(id=pid)
    user=request.user
    customer=reg_tbl.objects.get(user=user)
    obj=order.objects.create(user=customer,bike=bike,status='pending',date_added=datetime.datetime.today())
    obj.save()
    return redirect('view_order')

def view_order(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user
    # customer=reg_tbl.objects.filter(user=user)
    data=order.objects.filter(user__user=user)
    return render(request,'view_order.html',{'data':data})

def delete_order(request,bid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=order.objects.get(id=bid)
    obj.delete()
    return redirect('view_order')


def add_bikes(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    form = bikeForm()
    if request.method=='POST':
        form=bikeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_viewBikes')
    return render(request,'admin_add_bikes.html',{'form':form})

def add_comapny(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.method=='POST':
        form=companyForm(request.POST,request.FILES)
        # obj=companyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_allCompany')
    else:
        form=companyForm()
    return render(request,'add_company.html',{'form':form})

def add_type(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.method=='POST':
        form=typeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_allTypes')
    else:
        form=typeForm()
    return render(request,'add_type.html',{'form':form})

def view_detail(request,name):
    if not request.user.is_authenticated:
        return redirect('login')
    obj=bikes.objects.get(name=name)
    return render (request,'view_detail.html',{'bikes':obj})

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user
    data=reg_tbl.objects.get(user=user)
    return render(request,'user_profile.html',{'customer':data})

def edit_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user
    data=reg_tbl.objects.get(user=user)
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        u=request.POST['username']
        m=request.POST['mobile']
        loc=request.POST['location']
        data.user.first_name=f
        data.user.last_name=l
        data.user.username=e
        data.user_name=u
        data.mobile=m
        data.location=loc
        data.save()
        data.user.save()
        return redirect('user_profile')
    return render(request,'edit_user.html',{'customer':data})

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        p=request.POST['pwd']
        n=request.POST['npwd']
        c=request.POST['cpwd']
        # if n==c:
        id=request.user.id
        obj=User.objects.get(id=id)
        if obj.check_password(p):
            if n==c:
                obj.set_password(c)
                obj.save()
                error="no"#messages.success(request,'password changed successfully')
                # return redirect('login')
            else:
                messages.error(request,'new password and confirm password not matched')
        else:
            messages.error(request,'Please enter a valid password')
    d={'error':error}
    return render(request,'change_password.html',d)

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:

            if user.is_staff:
                login(request, user)

                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"

    d = {'error': error}
    return render(request, 'admin_login.html', d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    bike=bikes.objects.all()
    cmpy=company.objects.all()
    types=Type.objects.all()
    user=reg_tbl.objects.all()
    odr=order.objects.all()
    context={'bikes':bike,'company':cmpy,'type':types,'user':user,'order':odr}
    return render(request,'admin_home.html',context)

def admin_navigation(request):
    return render(request,'admin_navigation.html')

def admin_order(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=order.objects.all()
    return render(request,'admin_order.html',{'data':obj})

def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    data = order.objects.get(id=pid)
    if request.method == 'POST':
        s = request.POST['status']
        data.status = s
        try:
            data.save()
            error = "no"
        except:
            error = "yes"
    d = {'data': data, 'error': error}
    return render(request, 'change_status.html', d)

def admin_deleteorder(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=order.objects.get(id=id)
    obj.delete()
    return redirect('admin_order')
def admin_orderdetail(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    aa=order.objects.get(id=id)
    # data=reg_tbl.objects.get(user=user)
    # obj=bikes.objects.get(name=name)
    # context={'bikes':obj,'user':data}
    return render(request,'admin_orderdetail.html',{'data':aa})

def admin_deleteCustomer(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=User.objects.get(id=id)
    obj.delete()
    return redirect('admin_allCustomer')
    
def admin_allCustomer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=reg_tbl.objects.all()
    context={'data':obj}
    return render(request,'admin_allCustomer.html',context)

def admin_viewBikes(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=bikes.objects.all()
    return render(request,'admin_viewBikes.html',{'data':obj})

def admin_bikedetail(request,name):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=bikes.objects.get(name=name)
    return render(request,'admin_bikedetail.html',{'data':obj})

def admin_deleteBike(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=bikes.objects.get(id=id)
    obj.delete()
    return redirect('admin_viewBikes')

def admin_allCompany(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=company.objects.all()
    return render(request,'admin_allCompanies.html',{'data':obj})

def admin_deleteCompany(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=company.objects.get(id=id)
    obj.delete()
    return redirect('admin_allCompany')
def admin_allTypes(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=Type.objects.all()
    return render(request,'admin_allTypes.html',{'data':obj})

def admin_deleteType(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=Type.objects.get(id=id)
    obj.delete()
    return redirect('admin_allTypes')

def pending_orders(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=order.objects.filter(status='pending')
    return render(request,'admin_order.html',{'data':obj})

def accepted_orders(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=order.objects.filter(status='Accepted')
    return render(request,'admin_order.html',{'data':obj})

def rejected_orders(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=order.objects.filter(status='Rejected')
    return render(request,'admin_order.html',{'data':obj})

def admin_editbikes(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    obj=bikes.objects.get(id=id)
    form = bikeForm(instance=obj)
    if request.method=='POST':
        form=bikeForm(request.POST,request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('admin_viewBikes')
    return render(request,'admin_editbikes.html',{'form':form})
def search(request):
    # if 'q' in request.GET:
    q=request.GET['q']
    if q == "":
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        multiple_q=Q(Q(slug__icontains=q) |Q(company__slug__icontains=q)|Q(type__slug__icontains=q))
        data=bikes.objects.filter(multiple_q)
        if data:
            return render(request,'search.html',{'data':data})
        else:
            messages.info(request,'search result for '+q+' not found')
    return render(request,'search.html',{'data':data})

def about_us(request):
    return render(request,'about_us.html')

def contact_us(request):
    if request.method=='POST':
        email=request.POST['email'] 
        subject=request.POST['subject']       
        message=request.POST['message']
        send_mail(subject,message,settings.EMAIL_HOST_USER,[email],fail_silently=False)
        messages.success(request,'Email send successfully')
    return render(request,'contact.html')



        

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

