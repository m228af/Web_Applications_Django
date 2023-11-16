from django.shortcuts import render,redirect,get_object_or_404
from .form import *
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from .resources import StudentResource
from tablib import Dataset
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import status
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook
from django.shortcuts import render
from .models import Attendance  # Import the Attendance model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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








from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student

def enroll_fingerprint(request):
    if request.method == 'POST':
        fingerprint_data = request.POST.get('fingerprint_data', '')
        # You might need to process the fingerprint data as needed before storing it in the database.
        # Assuming you have a unique identifier for the student
        student_id = 'STUDENT_ID'  # Replace with the actual student ID

        try:
            # Check if the student already exists
            student = Student.objects.get(student_id=student_id)
            student.fprint1 = fingerprint_data
            student.save()
        except Student.DoesNotExist:
            # If the student doesn't exist, create a new one
            student = Student(student_id=student_id, fprint1=fingerprint_data)
            student.save()

        return JsonResponse({'message': 'Fingerprint data stored successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})







# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attendance

@api_view(['POST'])
def save_attendance(request):
    student_id = request.data.get('student_id')
    if not student_id:
        return Response({'error': 'Student ID is required.'}, status=400)

    attendance = Attendance(student_id=student_id)
    attendance.save()

    return Response({'success': True}, status=200)



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
    title = 'Add Student'
    form = StudentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            student = form.save(commit=False)  # Save the form data without committing to the database
            student.save()
            return redirect('capture_fingerprint', student_id=student.id)
    
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'insert_student.html', context)



from django.shortcuts import render, get_object_or_404
from student_registration.models import Student



from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .form import StudentForm
from .models import Student
from django.contrib import messages

@csrf_exempt
def capture_student(request):
    if request.method == 'POST':
        fingerprint_id = request.POST.get('fingerprint_id')
        fingerprint_data = {'fprint1': fingerprint_id}
        form = StudentForm(fingerprint_data)

        if form.is_valid():
            student = form.save()
            messages.success(request, 'Captured Successfully')
            response_data = {
                'status': 'success',
                'message': 'Student captured successfully',
                'student_id': student.id
            }
            return JsonResponse(response_data)
        else:
            response_data = {
                'status': 'error',
                'errors': form.errors.as_json()
            }
            return JsonResponse(response_data, status=400)
    elif request.method == 'GET':
        form = StudentForm()
        return render(request, 'insert_student.html', {'form': form})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)




def capture_fingerprint(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        # Process the captured fingerprint data
        fingerprint_data = request.POST.get('fprint1')
        
        # Update the student record with the captured fingerprint data
        student.fprint1 = fingerprint_data
        student.save()
        
        return redirect('student_list', student_id=student_id)
    
    context = {
        'student': student,
    }
    return render(request, 'enroll_prints.html', context)





from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def enroll_student(request):
    if request.method == 'POST':
        fingerprint_data = request.POST.get('fprint1', None)
        
        if fingerprint_data:
            # Save the fingerprint data in the specific field of your model
            student = Student.objects.create(fprint1=fingerprint_data)
            messages.success(request, 'Fingerprint data saved successfully')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Fingerprint data is missing'})
    else:
        return JsonResponse({'error': 'Only POST requests are supported for this endpoint.'}, status=405)
    


def student_list(request):
    title = 'Students Table'
    queryset = Student.objects.all()
    # Set the number of items per page
    items_per_page = 4
    # Create a Paginator instance
    paginator = Paginator(queryset, items_per_page)
    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        students = paginator.page(paginator.num_pages)

    student_count = Student.objects.count()
    context = {
        "title": title,
        "students": students,
        "student_count": student_count
    }

    return render(request, "student_list.html", context)




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
            )
            value.save()
        messages.success(request,'imported successfully')
        return student_list(request)



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




from django.http import JsonResponse
from .models import Student  # Import your Student model here

def get_student_info(request, student_id):
    try:
        # Assuming fingerprint_id is a unique identifier in your Student model
        student = Student.objects.get(fingerprint_id=student_id)

        # Retrieve relevant information from the student model
        student_info = {
            "student_id": student.student_id,
            "student_name": student.student_name,
            # Add other fields as needed
        }

        # Return the response as JSON
        return JsonResponse({"student_info": student_info})

    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)







#CRUD STUDENT========END

from django.db.models import Max
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from .models import Student, Module, Exam, Attendance

def clock_in(request):
    success_message = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')

        try:
            student = Student.objects.get(student_id=student_id)
            current_date = timezone.now().date()
            midnight_today = timezone.make_aware(timezone.datetime(current_date.year, current_date.month, current_date.day))

            matching_courses = Module.objects.filter(
                deg_code=student.deg_code,
                academic_level=student.student_level,
                semester=student.semester
            )

            last_clocked_in_course = Attendance.objects.filter(
                student=student,
                time_in__gte=midnight_today,
                time_out__isnull=True
            ).order_by('-time_in').first()

            if action == 'Clock In':
                clocked_in_flag = False

                for course in matching_courses:
                    is_scheduled = Exam.objects.filter(module_name=course, exam_date=current_date).exists()

                    if is_scheduled:
                        if last_clocked_in_course is None or last_clocked_in_course.module != course:
                            if not Attendance.objects.filter(
                                student=student,
                                module=course,
                                time_in__gte=midnight_today,
                                time_out__isnull=True
                            ).exists():
                                max_seat_number = Attendance.objects.filter(module=course, time_in__gte=midnight_today).aggregate(Max('seat_number'))['seat_number__max'] or 0

                                attendance = Attendance(
                                    student=student,
                                    module=course,
                                    time_in=timezone.now(),
                                    status="Present",
                                    seat_number=max_seat_number + 1
                                )
                                attendance.save()
                                messages.success(request, f'Clock In successful for course {course}. Your Seat Number is: {attendance.seat_number}')
                                # success_message = f'Clock In successful for course {course}. Your Seat Number is: {attendance.seat_number}'
                                last_clocked_in_course = attendance
                                clocked_in_flag = True
                            else:
                                messages.warning(request, f'You have already clocked in for course {course}.')
                                break
                if not clocked_in_flag:
                    messages.warning(request, 'No course scheduled for the day.')
            else:
                messages.warning(request, 'Invalid action.')
        except Student.DoesNotExist:
            messages.warning(request, 'Student does not exist.')
    return render(request, 'clock_in.html', {'success_message': success_message})



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


from django.shortcuts import render
from .models import Student, Module, Attendance

def expected_students(request, module_code):
    try:
        module = Module.objects.get(module_code=module_code)
        
        # Retrieve students enrolled in the specific module
        enrolled_students = Student.objects.filter(deg_code=module.deg_code, student_level=module.academic_level, semester=module.semester).order_by('student_name')
        
        # Create a dictionary to store attendance status for each student
        attendance_status = {}
        for student in enrolled_students:
            try:
                attendance = Attendance.objects.get(student=student, module=module)
                attendance_status[student] = attendance.status
            except Attendance.DoesNotExist:
                # If no attendance record is found, mark the student as "Absent"
                attendance_status[student] = "Absent"
        
    except Module.DoesNotExist:
        module = None
        enrolled_students = []
        attendance_status = {}

    return render(request, 'expected_students.html', {'enrolled_students': enrolled_students, 'module': module, 'attendance_status': attendance_status})







def search_students_by_module(request):
    if request.method == 'POST':
        form = ModuleSearchForm(request.POST)
        if form.is_valid():
            module_code = form.cleaned_data['module_code']
            return redirect('expected_students_for_course', module_code=module_code)
    else:
        form = ModuleSearchForm()
    return render(request, 'search_course.html', {'form': form})
    
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
    return redirect('timetable')  # Redirect to a different URL after deletion or GET request