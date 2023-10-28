from django.contrib import admin
from django.urls import path
from student_registration import views



urlpatterns=[
path('admin/', admin.site.urls),
# path('',views.access_control),
path('index/', views.Home, name='home'),
path('signup/', views.signup,name='signup'),
path('dashboard/', views.Dashboard, name='dashboard'),


path('api/',views.HelloApiView.as_view()),

#STUDENT CRUD OPERATION URLS


path('insert_student/',views.Student_Form, name='insert_student'),
path('student_list<int:id>', views.update_student, name='update_student'),
path('delete_student<int:id>/', views.delete_student, name='delete_student'),
path('import_student/', views.simple_upload, name='import_student'),
path('search/', views.search_student, name='search'),
path('student_list/',views.student_list,name='student_list'),


#INVIGILATOR CRUD OPERATION
path('insert_invigilator/',views.Invigilator_Form, name='insert_invigilator'),
path('invigilator_list<int:id>',views.update_invigilator,name='update_invigilator'),
path('delete_invigilator<int:id>/', views.delete_invigilator, name='delete_invigilator'),
path('search_invigilator/', views.search_invigilator, name='search_invigilator'),
path('invigilator_list/',views.invigilator_list,name='invigilator_list'),


#PROGRAM CRUD OPERATION URLS
path('insert_program/',views.Programme_Form, name='insert_program'),
path('program_list<int:id>/',views.update_program, name='update_program'),
path('delete_program<int:id>/', views.delete_program, name='delete_program'),
path('program_list/',views.program_list, name='program_list'),


#COURSE CRUD OPERATION
path('insert_course/',views.Course_Form, name='insert_course'),
path('course_list<int:id>/',views.update_course,name='update_course'),
path('course_list/',views.course_list,name='course_list'),
path('delete_course<int:id>/', views.delete_course, name='delete_course'),



#ROOM CRUD OPERATION
path('insert_room/',views.Room_Form, name='insert_room'),
path('room_list<int:id>/',views.update_room,name='update_room'),
path('room_list/',views.room_list,name='room_list'),
path('delete_room<int:id>/', views.delete_room, name='delete_room'),



#Exam Timetable 
path('create_timetable/',views.Exam_Form, name='create_timetable'),
path('timetable/',views.Timetable, name='timetable'),
path('timetable<int:id>/',views.update_exam,name='update_exam'),
path('delete_exam<int:id>/', views.delete_exam, name='delete_exam'),

#Attendance
path('examattendance/',views.get_attendance,name='exam_attendance'),
























# path('display_students/', views.count_students, name='count_students'),

path('insert_role/',views.Role_Form, name='insert_role'),
path('insert_user/',views.User_Form, name='insert_user'),



]