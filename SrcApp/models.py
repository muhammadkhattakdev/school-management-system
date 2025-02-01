from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.utils import timezone

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)  
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Fields required when using createsuperuser

    def __str__(self):
        return self.email  

class Teacher(models.Model):

    user = models.OneToOneField(to=MyUser, on_delete=models.CASCADE, verbose_name='Related User Model')

    def __str__(self):

        return self.user.first_name

class Course(models.Model):
    title = models.CharField(max_length=500, verbose_name="Course Title")
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, null=True)
    duration = models.PositiveIntegerField(default=0,null=False, verbose_name='Course Duration(in weeks)' )

    def __str__(self):

        return self.title
    

class Student(models.Model):
    courses = models.ManyToManyField(to=Course, verbose_name='Related Courses')
    user = models.OneToOneField(to=MyUser, on_delete=models.CASCADE, verbose_name='Related User Schema')
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, null=True, blank=True)
    faculty = models.CharField(max_length=2000, verbose_name="Faculty", null=False, default='')
    grade = models.CharField(max_length=200, verbose_name='Grade', null=False, default='')
    image = models.ImageField(upload_to='student_profile_images', default='', blank=True, null=True, verbose_name='Student Image')
    webcam_img = models.ImageField(upload_to='webcam_images', verbose_name='Webcam Image', null=True)

    def __str__(self):

        return self.user.first_name


class Attendance(models.Model):
    day = models.DateField(default=timezone.now)
    present_students = models.ManyToManyField(to=Student, null=True, blank=True, verbose_name="Present Students")
    teacher = models.ForeignKey(to=Teacher, on_delete=models.DO_NOTHING, verbose_name="Teacher")

    def __str__(self):

        return str(self.day)

