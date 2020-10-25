from django.db import models
from django.contrib.auth.models import User


class Mangement(models.Model):
    mangemen_name = models.CharField(max_length=150)

    def __str__(self):
        return self.mangemen_name
class EmportEmployee(models.Model):
    EmpID = models.IntegerField()
    EmpName = models.CharField(max_length =150)
    MangementId = models.IntegerField()

    def __str__(self):
        return self.EmpName
        
class Employee(models.Model):
    mangment = models.ForeignKey(Mangement,on_delete=models.CASCADE)
    user =  models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    moblie_no =models.CharField(max_length=15,null=False,blank=False,default=None)
    send_text = models.BooleanField(default=True)
    send_voice = models.BooleanField(default=True)
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Salary(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False)
    emmpname = models.CharField(max_length=250,blank =True, null=True)
    sMonth = models.IntegerField(blank=False,null=False)
    sYear = models.IntegerField(blank= False, null=False)
    base_salary = models.DecimalField(max_digits=9,decimal_places=3)
    total_salary = models.DecimalField(max_digits=9,decimal_places=3)        
    total_Diesc = models.DecimalField(max_digits=9,decimal_places=3)
    net_salary = models.DecimalField(max_digits=9,decimal_places=3)
    overtime = models.DecimalField(max_digits=9,decimal_places=3)
    health_care = models.DecimalField(max_digits=9,decimal_places=3)
    solfa1 = models.DecimalField(max_digits=9,decimal_places=3)
    solfa2 = models.DecimalField(max_digits=9,decimal_places=3)

    def __str__(self):
        return  self.sMonth, self.sYear


class Loan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    loan = models.DecimalField(max_digits=9,decimal_places=3)
    balance = models.DecimalField(max_digits=9,decimal_places=3)
    disc_amount = models.DecimalField(max_digits=9,decimal_places=3)

    def __str__(self):
        return self.user.first_name