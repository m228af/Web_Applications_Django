from django.contrib import admin
from django.urls import path
from student_registration import views



urlpatterns=[
path('admin/', admin.site.urls),
path('index/', views.Home, name='home'),
path('signup/', views.signup,name='signup'),

path('dashboard/', views.Dashboard, name='dashboard'),
path('insert_student/',views.Student_Form, name='insert_student'),
path('student_list<int:id>', views.update_student, name='update_student'),
path('delete_student<int:id>/', views.delete_student, name='delete_student'),
path('import_student/', views.simple_upload, name='import_student'),



path('insert_program/',views.Programme_Form, name='insert_program'),
path('insert_course/',views.Course_Form, name='insert_course'),
path('insert_role/',views.Role_Form, name='insert_role'),
path('insert_user/',views.User_Form, name='insert_user'),
path('insert_room/',views.Room_Form, name='insert_room'),
path('create_timetable/',views.Exam_Form, name='create_timetable'),
path('timetable/',views.Timetable, name='timetable'),
path('insert_invigilator/',views.Invigilator_Form, name='insert_invigilator'),


path('student_list/',views.student_list,name='student_list'),
path('course_list/',views.course_list,name='course_list'),
path('invigilator_list/',views.invigilator_list,name='invigilator_list'),





]