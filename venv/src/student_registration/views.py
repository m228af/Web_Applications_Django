from django.shortcuts import render,redirect,get_object_or_404
from .form import *
from .models import *
from django.contrib import messages
from django.utils import timezone

from django.http import HttpResponse

from openpyxl import load_workbook

from .resources import StudentResource
from tablib import Dataset





#Login Page
def Home(request):
    title='Biometric ExamGuard' 
    context={
        "title":title
    }
    return render(request,"index.html",context)

def signup(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
    else:
        form=RegisterForm()
    return render(request,"registration/signup.html",{"form":form})


#Home page
def Dashboard(request):
    title='Biometric Exam Guard'
    today = timezone.now().date() 
    student_count = Student.objects.count()
    exam_count=Exam.objects.filter(exam_date=today).count()
    invigilator_count=Invigilator.objects.count()
    context={
       "student_count":student_count,
       "exam_count":exam_count,
       "invigilator_count":invigilator_count
    }
    return render(request,"dashboard.html",context)

#CRUD STUDENT========START

def Student_Form(request):
    title='Add Student' 
    form=StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=StudentForm
        messages.success(request,'successfully submitted')
    context={
        "title":title,
        "form":form,
    }
    return render(request,"insert_student.html",context)


def student_list(request):
    title='Students Table' 
    queryset = Student.objects.all()
    context={"title":title,
            "queryset":queryset,
        }
    return render(request,"student_list.html",context)





def update_student(request, id):
    students=Student.objects.get(id=id) 
    form=StudentForm(request.POST or None,instance=students)
    if form.is_valid():
            form.save()
            return redirect('student_list')
    return render(request,'insert_student.html',{'form':form})


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)  # Fetch the student object by ID
    if request.method == 'POST':
        student.delete()  # Delete the student
        return redirect('student_list')  # Redirect to a success page or another URL after deletion
    # Handle GET request here if needed
    return redirect('student_list')  # Redirect to a different URL after deletion or GET request




# views.py
from django.shortcuts import render
from .models import Student

def search_student(request):
    students = Student.objects.all()  # Initialize with all students

    if request.method == 'POST':
        search_query = request.POST.get('custom_search_query')
        print(f"Search Query: {search_query}")  # Add this line for debugging
        if search_query:
            students = Student.objects.filter(student_id__icontains=search_query)
    return render(request, 'search.html', {'students': students})








##Count students to be displayed on the dashboard





##Upload CSV Files as alternative to manual data entry on the system

def simple_upload(request):
    if request.method=='POST':
        stu=StudentResource()
        ds=Dataset()
        new_stu=request.FILES['myFile']
        if not new_stu.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request,'student_list.html')
        imported_data=ds.load(new_stu.read(),format='xlsx')
        for data in imported_data:
            value=Student(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9], 
                data[10]
            )
            value.save()
            messages.success(request,'imported successfully')
        return student_list(request)




#CRUD STUDENT========END




#CRUD INVIGILATOR========START


def Invigilator_Form(request):
    title='Invilator' 
    form=InvigilatorForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=InvigilatorForm
        messages.success(request,'successfully submitted')
    context={
        "title":title,
        "form":form,
    }
    return render(request,"insert_invigilator.html",context)


def invigilator_list(request):
    title='Invigilators Table' 
    queryset = Invigilator.objects.all()
    context={"title":title,
            "queryset":queryset,
        }
    return render(request,"invigilator_list.html",context)



#CRUD INVIGILATOR========END








#CRUD PROGRAMMES========START

def Programme_Form(request):
    title='Add Programme' 
    form=DegreeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=DegreeForm
        messages.success(request,'successfully submitted')
    context={
        "title":title,
        "form":form,
    }
    return render(request,"insert_program.html",context)

#CRUD PROGRAMMES========END

#CRUD COURSES========START

def Course_Form(request):
    title='Add Course' 
    form=CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=CourseForm
        messages.success(request,'successfully submitted')
    context={
        "title":title,
        "form":form,
    }
    return render(request,"insert_course.html",context)



def course_list(request):
    title='Courses Table' 
    queryset = Module.objects.all()
    context={"title":title,
            "queryset":queryset,
        }
    return render(request,"course_list.html",context)



#CRUD COURSES========END



#CRUD USER ROLES========START
def Role_Form(request):
    title='Add User Role' 
    form=RoleForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=RoleForm
        messages.success(request,'successfully submitted')
    context={
        "title":title,
        "form":form,
    }
    return render(request,"insert_role.html",context)

#CRUD ROLES========END


#CRUD USERS========START
def User_Form(request):
    title='Add Users' 
    form=UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=UserForm
        messages.success(request,'successfully submitted')
    context={
        "title":title,
        "form":form,
    }
    return render(request,"insert_user.html",context)

#CRUD USERS========END


#CRUD ROOM========START
def Room_Form(request):
    title='Add Users' 
    form=RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=RoomForm
        messages.success(request,'successfully submitted')
    context={
        "title":title,
        "form":form,
    }
    return render(request,"insert_room.html",context)


#CRUD ROOM========END


#EXAMINATION CRUD ++++START

def Exam_Form(request):
    title='Time table' 
    form=ExaForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=ExaForm
        messages.success(request,'successfully submitted')
    context={
        "title":title,
        "form":form,
    }
    return render(request,"create_timetable.html",context)


def Timetable(request):
    title='Exam Time Table' 
    queryset = Exam.objects.all()
    context={"title":title,
            "queryset":queryset,
        }
    return render(request,"timetable.html",context)



