# Generated by Django 4.2.2 on 2023-07-09 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnquest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='title',
            field=models.CharField(default='Lesson 1', max_length=4096),
            preserve_default=False,
        ),
    ]