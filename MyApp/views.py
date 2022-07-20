# from email.mime import message
# from pyexpat import model
from django.http import Http404, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Car, Order, Contact

def index(request):
	return render(request,'index.html')

def about(request):
    return render(request,'about.html ')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        number = request.POST['number']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username = username).first():
            messages.error(request,"Username already taken")
            return redirect('register')
        if User.objects.filter(email = email).first():
            messages.error(request,"Email already taken")
            return redirect('register')

        if password != password2:
            messages.error(request,"Passwords do not match")
            return redirect('register')

        myuser = User.objects.create_user(username=username,email=email,password=password)
        myuser.name = name
        myuser.save()
        messages.success(request,"Your account has been successfully created!")
        return redirect('signin')


    else:
        print("error")
        return render(request,'register.html')
    

def signin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername,password = loginpassword)
        if user is not None:
            login(request, user)
            # messages.success(request,"Successfully logged in!")
            return redirect('vehicles')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('signin')

    else:
        print("error")
        return render(request,'login.html')

def signout(request):
        logout(request)
        # messages.success(request,"Successfully logged out!")
        return redirect('home')
    
    # return HttpResponse('signout')

def vehicles(request):
    cars = Car.objects.all()
    # print(cars)
    params = {'car':cars}
    return render(request,'vehicles.html ',params)

def bill(request):
    cars = Car.objects.all()
    params = {'cars':cars}
    return render(request,'bill.html',params)

def order(request):
    if request.method == "POST":
        billname = request.POST.get('billname','')
        billemail = request.POST.get('billemail','')
        billphone = request.POST.get('billphone','')
        billaddress = request.POST.get('billaddress','')
        billcity = request.POST.get('billcity','')
        cars11 = request.POST['cars11']
        dayss = request.POST.get('dayss','')
        date = request.POST.get('date','')
        fl = request.POST.get('fl','')
        tl = request.POST.get('tl','')
        # print(request.POST['cars11'])
        
        order = Order(name = billname,email = billemail,phone = billphone,address = billaddress,city=billcity,cars = cars11,days_for_rent = dayss,date = date,loc_from = fl,loc_to = tl)
        order.save()
        return redirect('home')
    else:
        print("error")
        return render(request,'bill.html')

def contact(request):
    if request.method == "POST":
        contactname = request.POST.get('contactname','')
        contactemail = request.POST.get('contactemail','')
        contactnumber = request.POST.get('contactnumber','')
        contactmsg = request.POST.get('contactmsg','')

        contact = Contact(name = contactname, email = contactemail, phone_number = contactnumber,message = contactmsg)
        contact.save()
    return render(request,'contact.html ')
