# Generated by Django 4.2.2 on 2023-07-09 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learnquest', '0002_lesson_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartCourses',
            new_name='CartCourse',
        ),
    ]
