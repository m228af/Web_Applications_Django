from student_registration import *
from django import forms
from .models import*
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        



class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields="__all__"
    # def __init__(self,*args,**kwargs):
    #     super(StudentForm,self).__init__(*args,**kwargs)
    #     self.fields['student_id'].required =False
class AttendanceForm(forms.ModelForm):
    class Meta:
        model=Attendnace
        fields="__all__"



class CourseForm(forms.ModelForm):
    class Meta:
        model=Module
        fields="__all__"

        
class InvigilatorForm(forms.ModelForm):
    class Meta:
        model=Invigilator
        fields="__all__"

class ExaForm(forms.ModelForm):
    class Meta:
        model=Exam
        fields = ['exam_date','exam_time','module_name','expected_candidates','room_name']
    exam_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields="__all__"

class RoleForm(forms.ModelForm):
    class Meta:
        model=Role
        fields="__all__"


class RoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields="__all__"


class DegreeForm(forms.ModelForm):
    class Meta:
        model=Degree
        fields="__all__"





class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)


class SearchInvigilator(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)




