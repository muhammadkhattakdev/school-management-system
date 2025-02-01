from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from .models import * 
import base64
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.files.base import ContentFile



def if_teacher(request):

    if request.user.user_type == 'teacher':
        return True
    return False

def if_student(request):

    if request.user.user_type == 'student':
        return True
    return False

@login_required(login_url='login')
def home(request):
    context = {}

    if if_teacher(request):
        return redirect('teacher_dashboard')
    else: 
        return redirect('student_home')


@login_required(login_url='login')
def teacher_dashboard_homepage(request):
    context = {}
    if not if_teacher(request):
        return redirect('login')
    user = request.user
    teacher = Teacher.objects.get(user=user)
    courses = Course.objects.filter(teacher=teacher)
    courses_count = courses.count()
    students = Course.objects.filter(teacher=teacher)
    students_count = students.count()

    context['courses'] = courses
    context['courses_count'] = courses_count
    context['students_count'] = students_count

    return render(request, 'teacherDashboard/home.html', context)

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            print("I'm here")
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            if user.user_type == 'teacher':
               
               return redirect('teacher_dashboard')  
            if user.user_type == 'student':
               return redirect('homepage')
        else:
            print('here')
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

@login_required(login_url='login')
def dashboard_students_page(request):
    if if_teacher(request):
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return redirect('login')

        students = Student.objects.filter(teacher=teacher)
        print(students)
        context = {
            'students': students,
        }
        return render(request, 'teacherDashboard/students.html', context)
    else:
        return redirect('login')


@csrf_exempt
@login_required(login_url='login')
def add_student(request):
    if request.method == "POST" and if_teacher(request):
        data = json.loads(request.body)
        try:
            teacher = Teacher.objects.get(user=request.user)

            # Create the student user
            student_user = MyUser.objects.create_user(
                username=data["email"],  # If `username` isn't used, replace with email
                email=data["email"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                user_type="student",
            )
            grade=data["grade"]
            faculty=data["faculty"]

            student = Student.objects.create(user=student_user, teacher=teacher,grade=grade, faculty=faculty,)

            return JsonResponse({"success": True, "message": "Student added successfully!"}, status=201)

        except Teacher.DoesNotExist:
            return JsonResponse({"success": False, "message": "Teacher not found."}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request."}, status=400)



def student_details(request, student_id):

    if not if_teacher(request):
        return redirect('login')

    context = {}

    student = Student.objects.get(id=student_id)
    user = request.user
    teacher = Teacher.objects.get(user=user)
    my_courses = Course.objects.filter(teacher=teacher)
    context['courses'] = my_courses
    context['student'] = student

    return render(request, 'teacherDashboard/studentDetails.html', context)


@login_required(login_url='login')
def update_student(request, student_id):
    if not if_teacher(request):
        return redirect('login')
    
    if request.method == "POST":
        student = get_object_or_404(Student, id=student_id)
        user = student.user

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        student.faculty = request.POST.get('faculty')
        student.grade = request.POST.get('grade')
        profile_img = request.FILES.get('profile_img')

        password = request.POST.get('password')
        if password:
            user.set_password(password)
        if profile_img is not None:
            student.image = profile_img

        user.save()

        course_ids = request.POST.getlist('courses')
        student.courses.set(course_ids)
        student.save()

        return redirect('student_details', student_id=student.id)

    return redirect('students_page')


@login_required
def courses(request):
    teacher = Teacher.objects.get(user=request.user)  
    courses = Course.objects.filter(teacher=teacher) 
    print(courses)
    return render(request, 'teacherDashboard/courses.html', {
        'courses': courses
    })



def add_course(request):
    if request.method == "POST":
        title = request.POST.get("title")
        duration = request.POST.get("duration")
        if title:
            user = request.user
            teacher = Teacher.objects.get(user=user)
            new_course = Course.objects.create(title=title, teacher=teacher, duration=duration)            
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Title is required"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required(login_url='login')
def course_details(request, course_id):

    if not if_teacher(request):
        return redirect('login')

    context = {}

    course = Course.objects.get(id=course_id)
    context['course'] = course

    return render(request, 'teacherDashboard/courseDetails.html', context)


@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        title = request.POST.get('course_title')
        duration = request.POST.get('course_duration')

        course.title = title
        course.duration = duration
        course.save()

        return redirect('courses')

    return redirect('edit_course', course_id=course.id)

from django.http import JsonResponse
from .models import Student


def search_students(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse([], safe=False)

    students = Student.objects.filter(
        user__first_name__icontains=query
    ) | Student.objects.filter(
        user__last_name__icontains=query
    ) | Student.objects.filter(
        user__email__icontains=query
    )

    student_data = [
        {
            'id': student.id,
            'first_name': student.user.first_name,
            'last_name': student.user.last_name,
            'email': student.user.email,
            'related_courses': [course.title for course in student.courses.all()],
        } for student in students
    ]

    return JsonResponse(student_data, safe=False)


@login_required
def search_courses(request):
    query = request.GET.get('q', '').strip()
    teacher = Teacher.objects.get(user=request.user)
    
    courses = Course.objects.filter(teacher=teacher, title__icontains=query)
    course_data = [{'id': course.id, 'title': course.title} for course in courses]
    return JsonResponse(course_data, safe=False)



@login_required(login_url='login')
def analytics(request):
    context = {}

    return render(request, 'teacherDashboard/analytics.html', context)



@login_required(login_url='login')
def student_homepage(request):

    if not if_student(request):
        return redirect('login')
    context = {}

    return render(request, 'studentPages/home.html', context)


from datetime import timedelta

@login_required(login_url='login')
def attendance_page(request):
    if not if_teacher(request):
        return redirect('login')

    today_date = timezone.now().date()
    teacher = Teacher.objects.get(user=request.user)

    # Ensure today's attendance object exists
    attendance, created = Attendance.objects.get_or_create(day=today_date, teacher=teacher)

    # Fetch attendance records from the past 7 days, including today
    start_date = today_date - timedelta(days=6)
    weekly_attendance = Attendance.objects.filter(day__range=[start_date, today_date], teacher=teacher)

    days_in_week = [start_date + timedelta(days=i) for i in range(7)]
    students = Student.objects.filter(teacher=teacher)


    attendance_data = []
    for student in students:
        student_attendance = []
        for day in days_in_week:
            attendance_record = weekly_attendance.filter(day=day, present_students=student).exists()
            student_attendance.append({
                'date': day,
                'present': attendance_record
            })
        attendance_data.append({
            'student': student,
            'attendance': student_attendance
        })

    context = {
        'attendance_data': attendance_data,
        'days_in_week': days_in_week,
        'today': today_date,
    }

    return render(request, 'teacherDashboard/attendance.html', context)


@login_required(login_url='login')
def update_attendance(request):
    if not if_teacher(request) or request.method != 'POST':
        return JsonResponse({'error': 'Unauthorized or invalid request'}, status=403)

    teacher = Teacher.objects.get(user=request.user)
    today_date = timezone.now().date()
    attendance = Attendance.objects.filter(day=today_date, teacher=teacher).first()

    if not attendance:
        return JsonResponse({'error': 'Attendance record not found'}, status=404)

    present_student_ids = request.POST.getlist('present_students[]')
    present_students = Student.objects.filter(id__in=present_student_ids, teacher=teacher)

    attendance.present_students.set(present_students)  # Clear and set new students
    attendance.save()

    return JsonResponse({'success': 'Attendance updated successfully'})


@login_required(login_url='login')
def student_profile(request):
    context = {}
    student = Student.objects.get(user=request.user)
    context['student'] = student
    print(student.grade)

    return render(request, 'studentPages/profile.html', context)



@login_required(login_url='login')
def update_student_profile(request, student_id):
    
    if request.method == "POST":
        print("Here am I khan g")
        student = get_object_or_404(Student, id=student_id)
        user = student.user

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        student.faculty = request.POST.get('faculty')
        student.grade = request.POST.get('grade')
        profile_img = request.FILES.get('profile_img')

        
        print(request.POST.get('grade'))
        password = request.POST.get('password')
        if password:
            user.set_password(password)

        if profile_img is not None:
            student.image = profile_img
            print(profile_img)

        user.save()

        course_ids = request.POST.getlist('courses')
        student.courses.set(course_ids)
        student.save()

        return redirect('student_home')

    return redirect('students_page')

@login_required(login_url='login')
def student_attendance_page(request):
    if not if_student(request):
        return redirect('login')

    # Fetch the current student object
    student = Student.objects.get(user=request.user)

    # Fetch all attendance records related to the student
    attendance_records = Attendance.objects.filter(present_students=student).order_by('day')

    # Get all unique attendance days, marking present or absent
    all_days = Attendance.objects.filter(teacher=student.teacher).values_list('day', flat=True).distinct().order_by('day')

    # Map attendance status for each day
    attendance_data = []
    for day in all_days:
        is_present = attendance_records.filter(day=day).exists()
        attendance_data.append({'day': day, 'status': 'Present' if is_present else 'Absent'})
    student = Student.objects.get(user=request.user)
    context = {
        'attendance_data': attendance_data,
        'student': student
    }

    return render(request, 'studentPages/attendance.html', context)

@login_required(login_url='login')
def take_attendance_page(request):
    context = {}

    return render(request, 'studentPages/takeAttendance.html', context)

@login_required(login_url='login')
def update_webcam_img(request):
    if request.method == 'POST':
        image_data = request.POST.get('imageData')
        if image_data:
            # Decode the base64 image
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_file = ContentFile(base64.b64decode(imgstr), name=f'webcam_capture.{ext}')
            print(image_file)
            # Update the student's webcam image 
            student = Student.objects.get(user=request.user)
            student.webcam_img.save(f"{request.user.username}_webcam.{ext}", image_file)
            student.save()
            print(student.webcam_img)
            return JsonResponse({'message': 'Image uploaded successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid request.'}, status=400)