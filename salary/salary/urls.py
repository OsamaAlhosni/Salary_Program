
from django.contrib import admin
from django.urls import path
from employee import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser,name='signupuser'),
    path('logout/', views.logoutuser,name='logoutuser'),
    path('login/', views.loginuser,name='loginuser'),    
    #Salary
    path('', views.home,name='home'),
    path('dash/', views.dashboard,name='dashboard'),

]
