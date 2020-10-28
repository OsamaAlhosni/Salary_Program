from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import EmportEmployee, Salary, Employee, Mangement


def home(request):
    return render(request, 'home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        if password2 == password:
            try:
                user = User.objects.create_user(username, password=password)
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'هذا الرقم الوظيفي سبق تسجيله بالمنظومة'})

        else:
            errmsg = 'كلمة المرور غير متطابقة'
            return render(request, 'signup.html', {'form': UserCreationForm(), 'error': errmsg})
# login user


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form': AuthenticationForm(), 'error': 'الرقم الوظيفي او كلمة المرور المدخلة غير صحيحين'})
        else:
            login(request, user)
            return redirect('dashboard')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def dashboard(request):
    user = request.user
    salary = Salary.objects.filter(user=user)

    total_salary = Salary.objects.filter(user=user)
    total_net_salary = 0
    total_solfa = 0
    total_overtime = 0
    total_healthcare = 0
    for qs in total_salary:
        total_net_salary += qs.net_salary
        total_solfa += qs.solfa1
        total_overtime += qs.overtime
        total_healthcare += qs.health_care
        print(total_net_salary)

    salary = {
        'total_salary': total_net_salary,
        'total_solfa': total_solfa,
        'total_overtime': total_overtime,
        'total_healthcare': total_healthcare

    }
    print(salary)
    return render(request, 'dash.html', salary)


def emport(request):
    if request.method == 'POST':
        password = 'password'
        employees = EmportEmployee.objects.all()
        for employee in employees:
            username = str(employee.EmpID)
            user = User.objects.create_user(
                username, password=password, first_name=employee.EmpName)
            user.save()
        return render(request, 'emport.html', {'Msg': 'Emport end'})
    else:
        return render(request, 'emport.html', {'Msg': 'Emport '})


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user = request.user
        mangemnts = Mangement.objects.all()
        employee = Employee.objects.filter(user=request.user)

        return render(request, 'profile.html', {'user': user, 'employee': employee, 'mangemnts': mangemnts})
