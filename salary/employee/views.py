from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import EmportEmployee, Salary, Employee, Mangement
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        # if request.method == 'GET':
        #     return render(request,'dash.html')
        # else:
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
        salary = {
            'total_salary': total_net_salary,
            'total_solfa': total_solfa,
            'total_overtime': total_overtime,
            'total_healthcare': total_healthcare

        }
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
    def update_email():
        email_user = User.objects.get(username=request.user.username)
        email_user.email = email
        email_user.save()

    if not request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'GET':
            user = request.user
            mangemnts = Mangement.objects.all()
            exits_profile, created = Employee.objects.get_or_create(
                user=request.user)
            if created:
                exits_profile.moblie_no = ''
                exits_profile.send_text = True
                exits_profile.send_voice = True
                exits_profile.send_email = True
                exits_profile.save()
            employee = Employee.objects.filter(user=request.user)
            return render(request, 'profile.html', {'user': user, 'employee': employee, 'mangemnts': mangemnts, 'error': 'خطأ'})
        else:
            mobile_no = request.POST['mobile-no']
            email = request.POST['email-input']
            mangement = request.POST['mangement']
            sms_checkbox = request.POST.get('sms-checkbox')
            voice_checkbox = request.POST.get('voice-checkbox')
            email_checkbox = request.POST.get('email-checkbox')
            user = request.user
            # set sms check box
            if not sms_checkbox:
                sms_checkbox = False
            else:
                sms_checkbox = True
            # set voice check box
            if not voice_checkbox:
                voice_checkbox = False
            else:
                voice_checkbox = True
            # set email check box
            if not email_checkbox:
                email_checkbox = False
            else:
                email_checkbox = True

            # if mangement == '0':
            #     return render(request, 'profile.html', {'error': 'يجب تحديد الإدارة التي تتبعها'})
            # else:
            mang = Mangement.objects.get(id=mangement)
            print(mangement)
            exits_profile, created = Employee.objects.get_or_create(
                user=request.user)
            if created:
                exits_profile.moblie_no = mobile_no
                exits_profile.send_text = True
                exits_profile.send_voice = True
                exits_profile.send_email = True
                exits_profile.mangment_id = mang.id
                exits_profile.save()
                update_email()

            print(exits_profile.moblie_no)
            if exits_profile:
                exits_profile.moblie_no = mobile_no
                exits_profile.send_text = True
                exits_profile.send_voice = True
                exits_profile.send_email = True
                exits_profile.mangment_id = mang.id
                exits_profile.save()
                update_email()
            else:
                profile_table = Employee(mangment_id=mang.id, user=request.user,
                                         moblie_no=mobile_no, send_text=True, send_voice=True, send_email=True)
                profile_table.save()
                update_email()
            return redirect('dashboard')


def views_salary(request):

    salarys_list = Salary.objects.filter(
        user=request.user).order_by('-sMonth', '-sYear')
    total_salary = 0
    for total in salarys_list:
        total_salary += total.net_salary
    page = request.GET.get('page', 1)

    paginator = Paginator(salarys_list, 4)
    try:
        salarys = paginator.page(page)
    except PageNotAnInteger:
        salarys = paginator.page(1)
    except EmptyPage:
        salarys = paginator.page(paginator.num_pages)

    return render(request, 'salary_view.html', {'salarys': salarys, 'total_salary': total_salary})


def salary(request, salary_pk):
    salary = get_object_or_404(Salary, pk=salary_pk, user=request.user)
    # salary = Salary.objects.filter(id=salary_pk)
    return render(request, 'salary.html', {'salary': salary})
