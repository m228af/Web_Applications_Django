from django.shortcuts import render,redirect,get_object_or_404
from .form import *
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import load_workbook
from .resources import StudentResource
from tablib import Dataset

from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import status



from django.utils import timezone
from datetime import timedelta
from django.contrib import messages




from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.shortcuts import render
from .models import Attendance  # Import the Attendance model









from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handle_http_request(request):
    if request.method == 'GET':
        # Process GET request data
        data = {'message': 'GET request received'}
    elif request.method == 'POST':
        # Process POST request data
        data = {'message': 'POST request received'}
    else:
        data = {'message': 'Unsupported request method'}
    return JsonResponse(data)







"""APIs."""
class HelloApiView(APIView):

    serializer_class=serializers.HelloSerializer
    def get(self,request,format=None):
        an_apiview=[

            'Hey Programmer',
            'Thanks for Trying',
            'Everything is gona be ok'
        ]
        return Response({'message':'Hello Anesu','an_apiview':an_apiview})
    
    def post(self,request):
        serializer=serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name=serializer.data.get('name')
            message='Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

    def put(self,request,pk=None):

        return Response({'method':'put'})
    

    def patch(self,request,pk=None):

        return Response({'method':'patch'})
    
    def delete(self,request,pk=None):

        return Response({'method':'delete'})




#Login Page

def access_control(request):
    if request.method=='POST':
        if request.POST.get('student_num'):
            post=Attendance()
            post.student_id=request.POST.get('student_num')
            post.save()    
    return render(request,"access_control.html")



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
       "invigilator_count":invigilator_count,
       "today":today
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
    student_count = Student.objects.count()

    context={"title":title,
            "queryset":queryset,
            "student_count":student_count

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



from django.shortcuts import render
from .models import Student, Module

def search_student(request):
    form = SearchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        search_query = form.cleaned_data['search_query']
        records = Student.objects.filter(student_id__icontains=search_query)
        context = {"form": form, "records": records}
        if records:
            student = records[0]
            academic_level = student.student_level
            semester = student.semester
            student_program = student.deg_code  # Assuming deg_code points to the program
            courses = Module.objects.filter(academic_level=academic_level, semester=semester, deg_code=student_program)
            context['student'] = student
            context['courses'] = courses
        return render(request, 'search.html', context)
    return render(request, 'search.html', {"form": form})









def display_attendance_list(request, course_name):
    course = Module.objects.get(course_name=course_name)  # Assuming you have a course name in the URL or as a parameter
    attended_students = Student.objects.filter(attendance__course=course)
    academic_level = course.academic_level
    degree_program = course.deg_code
    all_students = Student.objects.filter(student_level=academic_level, deg_code=degree_program)
    not_attended_students = all_students.exclude(id__in=attended_students.values_list('id', flat=True))
    context = {
        'attended_students': attended_students,
        'not_attended_students': not_attended_students,
        'course_name': course_name,
    }
    return render(request, 'attendance.html', context)


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
    





from .models import Student, Module

def search_student_by_course(request):
    form = SearchStudents(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        course_code_str = form.cleaned_data['module_code']  # Assuming course_code is a string representing the course code
        # Find the corresponding course object based on the course code
        try:
            course_code = Module.objects.get(course_code=course_code_str)
        except Module.DoesNotExist:
            # Handle the case where the course code does not exist
            course_code = None

        if course_code:
            # Filter students based on the course's academic level, semester, and program
            students = Student.objects.filter(
                academic_level=course_code.academic_level,
                semester=course_code.semester,
                deg_code=course_code.deg_code  # Assuming deg_code points to the program
            )

            # Fetch all courses related to the provided academic level, semester, and program
            courses = Module.objects.filter(
                academic_level=course_code.academic_level,
                semester=course_code.semester,
                deg_code=course_code.deg_code
            )
        else:
            students = []
            courses = []

        context = {"form": form, "students": students, "courses": courses}

        return render(request, 'search_by_course.html', context)

    return render(request, 'search_by_course.html', {"form": form})






#CRUD STUDENT========END



#Attendance 


from django.utils import timezone
from datetime import datetime

def clock_in(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')
        form = AttendanceForm()
        try:
            student = Student.objects.get(student_id=student_id)
            if action == 'Clock In':
                # Check if the student is already clocked in
                attendance = Attendance.objects.filter(student=student, time_out__isnull=True).first()
                if attendance:
                    messages.warning(request, 'You are already clocked in for a course.')
                else:
                    # Get the current date
                    current_date = timezone.now().date()
                    
                    # Filter Module instances that match the student's degree, academic level, and semester
                    matching_courses = Module.objects.filter(
                        deg_code=student.deg_code,
                        academic_level=student.student_level,
                        semester=student.semester
                    )

                    # Iterate through matching courses to check for attendance
                    for course in matching_courses:
                        # Check if attendance exists for the student in the current course and date
                        existing_attendance = Attendance.objects.filter(student=student, module=course, time_in__date=current_date).first()
                        
                        if not existing_attendance:
                            # Create a new attendance record for the student in this course
                            attendance = Attendance(student=student, module=course, time_in=timezone.now(), status="Present")
                            attendance.save()
                            messages.success(request, 'Clock In successful for course.')                    
                    # If all matching courses already have attendance records
                    messages.warning(request, 'No available courses to clock in for this student on this date.')
        except Student.DoesNotExist:
            messages.warning(request, 'Student does not exist.')
        return redirect('clock_in')
    return render(request, 'clock_in.html')






def clock_out(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Student.objects.get(student_id=student_id)
            try:
                attendance = Attendance.objects.get(student=student, time_out__isnull=True)
                attendance.time_out = timezone.now()
                attendance.save()
                messages.success(request, 'Clock Out successful for course.')
            except Attendance.DoesNotExist:
                messages.warning(request, 'You cannot clock out without a previous clock-in.')
        except Student.DoesNotExist:
            messages.warning(request, 'Student does not exist.')
        return redirect('clock_out')
    return render(request, 'clock_out.html')


def view_attendance(request):
    # Retrieve attendance records from the database
    attendance_records = Attendance.objects.select_related('student')

    # Pass the attendance records to the template
    context = {
        'attendance_records': attendance_records
    }

    return render(request, 'attendance.html', context)

def Attendance_Form(request):
    form=AttendanceForm(request.POST or None)
    stu=Student.objects.filter(deg_code=1)
    if form.is_valid():
        form.save()
        form=AttendanceForm
        messages.success(request,'successfully submitted')
    context={
        
        "form":form,
    }
    return render(request,"preloader.html",context)



def export_attendance_to_excel(request):
    # Retrieve attendance data from your model
    attendance_data = Attendance.objects.all()

    # Create an Excel workbook and add data to it
    workbook = Workbook()
    sheet = workbook.active

    # Define the headers
    sheet.append(["Student ID", "Time In", "Time Out", "Module", "Status"])

    # Add data from the Attendance model
    for entry in attendance_data:
        # Convert datetime objects to strings without timezone information
        time_in = entry.time_in.strftime('%Y-%m-%d %H:%M:%S')
        time_out = entry.time_out.strftime('%Y-%m-%d %H:%M:%S') if entry.time_out else ''
        
        sheet.append([entry.student.student_id, time_in, time_out, entry.module.module_name, entry.status])

    # Create a response for downloading the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=attendance.xlsx'

    # Save the workbook content to the response
    workbook.save(response)

    return response


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





#Assign courses for students



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



