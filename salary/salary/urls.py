
from django.contrib import admin
from django.urls import path
from employee import views
from emport_salary import views as salaryviews

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    # Salary
    path('', views.home, name='home'),
    path('dash/', views.dashboard, name='dashboard'),
    path('emport/', views.emport, name='emport'),
    path('profile/', views.profile, name='profile'),
    path('loan/', views.loan, name='loan'),
    path('views_salary/', views.views_salary, name='views_salary'),
    path('health_care/', views.health_care, name='health_care'),
    path('salary/<int:salary_pk>', views.salary, name='salary'),
    path('resultdata/', views.resultdata, name='resultdata'),
    path('changepass/', views.change_password, name='change_password'),

]
