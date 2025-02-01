from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import * 

class CustomUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'username', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'user_type', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'user_type', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', )

    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email Address'

# class StudentAdmin(admin.ModelAdmin):

#     list_display = ('email', 'first_name')

#     def first_name(self, obj):
#         return obj.user.first_name
#     first_name.short_description = 'First Name'

#     def email(self, obj):

#         return obj.user.email
#     email.short_description = "Email Address"




# class AttendanceAdmin(admin.ModelAdmin):

#     list_display = ['day']

admin.site.register(Teacher, TeacherAdmin)
# admin.site.register(Attendance, AttendanceAdmin)
# admin.site.register(Student, StudentAdmin)

admin.site.register(MyUser, CustomUserAdmin)
