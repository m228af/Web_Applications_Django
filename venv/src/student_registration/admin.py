from django.contrib import admin
from student_registration.models import *
from student_registration.form import *

from import_export.admin import ImportExportModelAdmin


# Register your models here.
class StudentAdmin(ImportExportModelAdmin):
    list_display=[
                 "student_id",
                 "student_name",
                 "student_gender",  
                 "student_email",
                 "student_nationalId",
                 "student_birth_date",
                 "deg_code",
                 "user_role",
                 "student_level",
                 "semester",
                 ]
    
    form=StudentForm
    list_filter=['student_id']
    search_fields=['student_id']



class AttendanceAdmin(admin.ModelAdmin):
    list_display=[
                 "student_id",
                 "clock_in",
                 "clock_out",
                 ]
    
    form=AttendanceForm
    list_filter=['student_id','clock_in','clock_out']
    search_fields=['student_id']




admin.site.register(Student,StudentAdmin)
admin.site.register(Role)
admin.site.register(Room)
admin.site.register(Invigilator)
admin.site.register(Exam)
admin.site.register(Degree)
admin.site.register(Module)
# admin.site.register(StudentCourses)
admin.site.register(Attendance)


