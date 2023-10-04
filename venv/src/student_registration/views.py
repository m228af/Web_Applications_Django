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
            messages.success(request,'Updated Successfully')
            return redirect('student_list')
    return render(request,'insert_student.html',{'form':form})


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)  # Fetch the student object by ID
    if request.method == 'POST':
        student.delete()  # Delete the student
        messages.success(request,'Deleted Successfully')
        return redirect('student_list')  # Redirect to a success page or another URL after deletion
    # Handle GET request here if needed
    return redirect('student_list')  # Redirect to a different URL after deletion or GET request


def search_student(request):
    if request.method == 'POST':
        form = SearchForm(request.POST or None)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            records = Student.objects.filter(student_id__icontains=search_query)
            return render(request, 'search.html', {'form': form, 'records': records})
    else:
        form = StudentForm
    return render(request, 'search.html', {'form': form})



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





def update_invigilator(request, id):
    invigilator=Invigilator.objects.get(id=id) 
    form=InvigilatorForm(request.POST or None,instance=invigilator)
    if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('invigilator_list')
    return render(request,'insert_invigilator.html',{'form':form})


def delete_invigilator(request, id):
    invigilator = get_object_or_404(Invigilator, id=id)  
    if request.method == 'POST':
        invigilator.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('invigilator_list')  
    return redirect('invigilator_list') 

def search_invigilator(request):
    if request.method == 'POST':
        form = SearchInvigilator(request.POST or None)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            records = Invigilator.objects.filter(emp_id__icontains=search_query)
            return render(request, 'search_invigilator.html', {'form': form, 'records': records})
    else:
        form = InvigilatorForm
    return render(request, 'search_invigilator.html', {'form': form})



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


def program_list(request):
    title='List of Programmes' 
    queryset = Degree.objects.all()
    context={"title":title,
            "queryset":queryset,
        }
    return render(request,"program_list.html",context)



def update_program(request, id):
    degree=Degree.objects.get(id=id) 
    form=DegreeForm(request.POST or None,instance=degree)
    if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('program_list')
    return render(request,'insert_program.html',{'form':form})


def delete_program(request, id):
    program = get_object_or_404(Degree, id=id)  # Fetch the student object by ID
    if request.method == 'POST':
        program.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('program_list')  # Redirect to a success page or another URL after deletion
    # Handle GET request here if needed
    return redirect('program_list')  # Redirect to a different URL after deletion or GET request











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




def update_course(request, id):
    course=Module.objects.get(id=id) 
    form=CourseForm(request.POST or None,instance=course)
    if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('course_list')
    return render(request,'insert_course.html',{'form':form})


def delete_course(request, id):
    course = get_object_or_404(Module, id=id)  # Fetch the student object by ID
    if request.method == 'POST':
        course.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('course_list')  # Redirect to a success page or another URL after deletion
    # Handle GET request here if needed
    return redirect('course_list')  # Redirect to a different URL after deletion or GET request




#CRUD COURSES========END


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


def room_list(request):
    title='List of Exam Venue' 
    queryset = Room.objects.all()
    context={"title":title,
            "queryset":queryset,
        }
    return render(request,"room_list.html",context)

def update_room(request, id):
    room=Room.objects.get(id=id) 
    form=RoomForm(request.POST or None,instance=room)
    if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('room_list')
    return render(request,'insert_room.html',{'form':form})


def delete_room(request, id):
    room = get_object_or_404(Room, id=id)  # Fetch the student object by ID
    if request.method == 'POST':
        room.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('room_list')  # Redirect to a success page or another URL after deletion
    # Handle GET request here if needed
    return redirect('room_list')  # Redirect to a different URL after deletion or GET request









#CRUD ROOM========END



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



def update_exam(request, id):
    exam=Exam.objects.get(id=id) 
    form=ExaForm(request.POST or None,instance=exam)
    if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('timetable')
    return render(request,'create_timetable.html',{'form':form})


def delete_exam(request, id):
    exam = get_object_or_404(Exam ,id=id)  # Fetch the student object by ID
    if request.method == 'POST':
        exam.delete() 
        messages.success(request,'Deleted Successfully')
        return redirect('timetable')  # Redirect to a success page or another URL after deletion
    # Handle GET request here if needed
    return redirect('timetable')  # Redirect to a different URL after deletion or GET request



