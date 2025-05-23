# Generated by Django 5.1.5 on 2025-01-29 10:24

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SrcApp', '0010_course_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(default=django.utils.timezone.now)),
                ('present_students', models.ManyToManyField(blank=True, null=True, to='SrcApp.student', verbose_name='Present Students')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='SrcApp.teacher', verbose_name='Teacher')),
            ],
        ),
    ]
