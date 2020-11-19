from django.contrib import admin

from .models import Salary, Loan, Mangement, Employee


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'sMonth', 'sYear', 'net_salary',
                    'overtime', 'health_care', 'solfa1', 'solfa2')
    ordering = ('user', 'sMonth', 'sYear')
    # search_fields = ('user', 'sMonth', 'sYear')


admin.site.register(Loan)
admin.site.register(Mangement)
admin.site.register(Employee)
