# Generated by Django 5.1.5 on 2025-01-28 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SrcApp', '0007_remove_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SrcApp.teacher'),
        ),
    ]
