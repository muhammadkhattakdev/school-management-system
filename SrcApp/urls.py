from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('teacher_dashboard/', views.teacher_dashboard_homepage, name='teacher_dashboard'),
    path('login/', views.login_user, name='login'),
    path('teacher_dashboard/students/', views.dashboard_students_page, name='students'),
    path('add-student/', views.add_student, name='add_student'),
    path('teacher_dashboard/students/<student_id>', views.student_details, name='student_details' ),
    path('teacher_dashboard/update_student/<int:student_id>/', views.update_student, name='update_student'),
    path('teacher_dashboard/courses/', views.courses, name='courses'),
    path('add-course/', views.add_course, name='add_course'),
    path('teacher_dashboard/course-details/<course_id>', views.course_details, name='course_details'),
    path('teacher_dashboard/course/<int:course_id>/edit/', views.update_course, name='update_course'),
    path('teacher_dashboard/students/search/', views.search_students, name='search_students'),
    path('teacher_dashboard/courses/search/', views.search_courses, name='search_courses'),
    path('teacher_dashboard/analytics/', views.analytics, name='analytics'),
    path('teacher_dashboard/attendance/', views.attendance_page, name='attendance'),
    path('teacher_dashboard/attendance/update/', views.update_attendance, name='update_attendance'),



    path('student/', views.student_homepage, name='student_home'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/update_student_profile/<int:student_id>/', views.update_student_profile, name='update_student_profile'),
    path('student/attendance/', views.student_attendance_page, name='student_attendance_page'),
    path('student/take-attendance/', views.take_attendance_page, name='take_attendance_page'),
    path('student/update-webcam-img/', views.update_webcam_img, name='update_webcam_img'),
]