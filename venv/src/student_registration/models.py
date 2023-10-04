from django.db import models


# Create your models here.

class Gender(models.TextChoices):
    Male='Male'
    Female='Female'



class Role(models.Model):
    user_role=models.CharField("ROLE",max_length=255,unique=True)
    def __str__(self):
        return self.user_role
    



class Degree(models.Model):
    deg_code=models.CharField(max_length=255,unique=True)
    deg_name=models.CharField(max_length=255)

    def __str__(self):
        return self.deg_name
    




class Module(models.Model):
    module_code=models.CharField("COURSE CODE",max_length=255,unique=True)
    module_name=models.CharField("COURSE NAME",max_length=255,unique=True)
    deg_code=models.ForeignKey(Degree, on_delete=models.CASCADE)
    def __str__(self):
        return self.module_name
    



# class User(models.Model):
#     user_name=models.CharField("LOGIN NAME",max_length=25,unique=True)
#     user_fullname=models.CharField("FULL NAME",max_length=30,unique=True)
#     user_role=models.ForeignKey(Role,on_delete=models.CASCADE)
#     user_password=models.CharField("PASSWORD",max_length=25)
#     confirm_password=models.CharField("CONFIRM PASSWORD",max_length=25)
#     def __str__(self):
#         return self.login_name


class Student(models.Model):
    student_id=models.CharField("STUDENT ID",max_length=30)
    student_name=models.CharField("FULL NAME",max_length=255)
    student_gender=models.CharField("GENDER",max_length=10,choices=Gender.choices)
    student_email=models.CharField("EMAIL ADDRESS",max_length=30,unique=True)
    student_nationalId=models.CharField("NATIONAL ID",max_length=30,unique=True)
    student_birth_date=models.DateField("D.O.B",auto_now_add=False, auto_now=False, blank=False,null=False)
    deg_code=models.ForeignKey(Degree, on_delete=models.CASCADE)
    user_role=models.ForeignKey(Role,on_delete=models.CASCADE)
    student_level=models.IntegerField("ACADEMIC LEVEL")
    semester=models.IntegerField("SEMESTER")
    def __str__(self):
        return self.student_id
    




    


    
class Invigilator(models.Model):
    emp_id=models.CharField("EC No or EMPLOYEE ID",max_length=30)
    emp_name=models.CharField("FULL NAME",max_length=30)
    emp_gender=models.CharField("GENDER",max_length=10,choices=Gender.choices)
    empt_email=models.CharField("EMAIL ADDRESS",max_length=30)
    emp_nationalId=models.CharField("NATIONAL ID",max_length=30,unique=True)
    user_role=models.ForeignKey(Role,on_delete=models.CASCADE)
    def __str__(self):
        return self.emp_id+' '+self.emp_name
    
class Room(models.Model):
    room_code=models.CharField(max_length=25,unique=True)
    room_name=models.CharField(max_length=25,unique=True)
    room_capacity=models.IntegerField()

    def __str__(self):
        return self.room_code+' '+self.room_name
    


class Exam(models.Model):
    exam_date=models.DateField(auto_now_add=False, auto_now=False, blank=False,null=False)
    exam_time=models.TimeField()
    module_name=models.ForeignKey(Module,on_delete=models.CASCADE)
    expected_candidates=models.IntegerField()
    room_name=models.ForeignKey(Room,on_delete=models.CASCADE)
    def __str__(self):
        return self.exam_date

# class RegisterStudent(models.Model):
#     student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
#     reg_status=models.CharField(max_length=20)
#     student_level=models.ForeignKey(Student,on_delete=models.CASCADE)
#     semester=models.ForeignKey(Student,on_delete=models.CASCADE)
    


    





