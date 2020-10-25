from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import EmportEmployee

def home(request):
    return render(request,'home.html')
    
def signupuser(request):
    if request.method == 'GET':
       return render(request,'signup.html',{'form':UserCreationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        if password2 == password:
            try:
                user = User.objects.create_user(username,password=password)
                user.save()
                login(request,user)
                return redirect('dashboard')
            except IntegrityError: 
                return render(request,'signup.html',{'form':UserCreationForm(),'error':'هذا الرقم الوظيفي سبق تسجيله بالمنظومة'})
                 
        else:
            errmsg = 'كلمة المرور غير متطابقة'
            return render(request,'signup.html',{'form':UserCreationForm(),'error':errmsg})
# login user            
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form':AuthenticationForm(), 'error':'الرقم الوظيفي او كلمة المرور المدخلة غير صحيحين'})
        else:
            login(request, user)
            return redirect('dashboard')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def dashboard(request):
    return render(request,'dash.html')

def emport(request):
    if request.method == 'POST':
        password = 'password'
        employees = EmportEmployee.objects.all()
        for employee in employees:
            username = str(employee.EmpID)
            user = User.objects.create_user(username,password=password,first_name = employee.EmpName)
            user.save()
        return render(request,'emport.html',{'Msg': 'Emport end'})
    else:
        return render(request,'emport.html',{'Msg': 'Emport '})